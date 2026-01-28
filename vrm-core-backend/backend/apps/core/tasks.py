from celery import shared_task
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .models import Evidence, Assessment, Renewal, AuditLog

import logging

logger = logging.getLogger(__name__)


@shared_task
def evidence_expiry_reminder():
    """
    Send reminders for evidence expiring in 30, 15, and 7 days
    """
    today = timezone.now().date()
    reminder_days = [30, 15, 7]
    
    for days in reminder_days:
        target_date = today + timedelta(days=days)
        expiring_evidence = Evidence.objects.filter(
            expiry_date=target_date,
            is_expired=False
        ).select_related('assessment__vendor', 'assessment__org', 'uploaded_by')
        
        for evidence in expiring_evidence:
            try:
                # Log the reminder
                AuditLog.objects.create(
                    org=evidence.assessment.org,
                    actor=None,
                    action='update',
                    entity_type='evidence',
                    entity_id=evidence.id,
                    changes={'reminder_sent': f'{days} days before expiry'}
                )
                
                # Send email notification
                send_evidence_expiry_email(evidence, days)
                logger.info(f"Evidence expiry reminder sent for {evidence.id} ({days} days)")
                
            except Exception as e:
                logger.error(f"Failed to send evidence expiry reminder: {str(e)}")
    
    return f"Processed evidence expiry reminders for days: {reminder_days}"


@shared_task
def renewal_due_reminder():
    """
    Send reminders for upcoming and overdue renewals
    """
    today = timezone.now().date()
    
    # Find renewals due within next 30 days
    upcoming_renewals = Renewal.objects.filter(
        status__in=['pending', 'triggered'],
        due_date__gte=today,
        due_date__lte=today + timedelta(days=30)
    ).select_related('assessment__vendor', 'assessment__org')
    
    for renewal in upcoming_renewals:
        try:
            days_until_due = (renewal.due_date - today).days
            
            # Log the reminder
            AuditLog.objects.create(
                org=renewal.assessment.org,
                actor=None,
                action='renewal_trigger',
                entity_type='renewal',
                entity_id=renewal.id,
                changes={'days_until_due': days_until_due}
            )
            
            # Send email notification
            send_renewal_reminder_email(renewal, days_until_due)
            logger.info(f"Renewal reminder sent for {renewal.id} ({days_until_due} days)")
            
        except Exception as e:
            logger.error(f"Failed to send renewal reminder: {str(e)}")
    
    # Find overdue renewals
    overdue_renewals = Renewal.objects.filter(
        status__in=['pending', 'triggered'],
        due_date__lt=today
    ).select_related('assessment__vendor', 'assessment__org')
    
    for renewal in overdue_renewals:
        try:
            renewal.status = 'overdue'
            renewal.save()
            
            # Log the overdue status
            AuditLog.objects.create(
                org=renewal.assessment.org,
                actor=None,
                action='update',
                entity_type='renewal',
                entity_id=renewal.id,
                changes={'status': 'overdue'}
            )
            
            send_renewal_overdue_email(renewal)
            logger.info(f"Renewal marked overdue for {renewal.id}")
            
        except Exception as e:
            logger.error(f"Failed to mark renewal overdue: {str(e)}")
    
    return f"Processed {upcoming_renewals.count()} upcoming and {overdue_renewals.count()} overdue renewals"


@shared_task
def assessment_due_reminder():
    """
    Send reminders for assessments due soon
    """
    today = timezone.now()
    
    # Find assessments due within next 7 days
    due_assessments = Assessment.objects.filter(
        status__in=['assigned', 'in_progress'],
        due_date__gte=today,
        due_date__lte=today + timedelta(days=7)
    ).select_related('vendor', 'org', 'assigned_by')
    
    for assessment in due_assessments:
        try:
            days_until_due = (assessment.due_date - today).days
            
            # Log the reminder
            AuditLog.objects.create(
                org=assessment.org,
                actor=None,
                action='update',
                entity_type='assessment',
                entity_id=assessment.id,
                changes={'days_until_due': days_until_due}
            )
            
            send_assessment_due_email(assessment, days_until_due)
            logger.info(f"Assessment due reminder sent for {assessment.id} ({days_until_due} days)")
            
        except Exception as e:
            logger.error(f"Failed to send assessment due reminder: {str(e)}")
    
    return f"Processed {due_assessments.count()} due assessments"


@shared_task
def mark_expired_evidence():
    """
    Daily task to mark evidence as expired and create audit logs
    """
    today = timezone.now().date()
    expired_evidence = Evidence.objects.filter(
        expiry_date__lt=today,
        is_expired=False
    ).select_related('assessment__org')
    
    count = 0
    for evidence in expired_evidence:
        try:
            evidence.is_expired = True
            evidence.save()
            
            AuditLog.objects.create(
                org=evidence.assessment.org,
                actor=None,
                action='update',
                entity_type='evidence',
                entity_id=evidence.id,
                changes={'is_expired': True}
            )
            count += 1
            
        except Exception as e:
            logger.error(f"Failed to mark evidence expired: {str(e)}")
    
    logger.info(f"Marked {count} evidence items as expired")
    return f"Marked {count} evidence items as expired"


# Helper functions for sending emails

def send_evidence_expiry_email(evidence, days):
    """Send evidence expiry reminder email"""
    subject = f"Evidence Expiring in {days} Days"
    message = f"""
    Dear {evidence.uploaded_by.django_user.first_name},

    The following evidence will expire in {days} days:
    
    File: {evidence.file_name}
    Assessment: {evidence.assessment.vendor.name}
    Expiry Date: {evidence.expiry_date}
    
    Please ensure to renew or replace this evidence before it expires.

    Best regards,
    VRM System
    """
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [evidence.uploaded_by.django_user.email],
        fail_silently=True
    )


def send_renewal_reminder_email(renewal, days_until_due):
    """Send renewal reminder email"""
    subject = f"Assessment Renewal Due in {days_until_due} Days"
    message = f"""
    Dear Administrator,

    The following assessment renewal is due in {days_until_due} days:
    
    Vendor: {renewal.assessment.vendor.name}
    Assessment: {renewal.assessment.template.name}
    Due Date: {renewal.due_date}
    
    Please trigger the renewal process.

    Best regards,
    VRM System
    """
    
    # Send to all org admins
    admins = renewal.assessment.org.users.filter(role='admin')
    for admin in admins:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [admin.django_user.email],
            fail_silently=True
        )


def send_renewal_overdue_email(renewal):
    """Send renewal overdue email"""
    subject = "Assessment Renewal OVERDUE"
    message = f"""
    Dear Administrator,

    The following assessment renewal is OVERDUE:
    
    Vendor: {renewal.assessment.vendor.name}
    Assessment: {renewal.assessment.template.name}
    Due Date: {renewal.due_date}
    
    Please take immediate action.

    Best regards,
    VRM System
    """
    
    # Send to all org admins
    admins = renewal.assessment.org.users.filter(role='admin')
    for admin in admins:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [admin.django_user.email],
            fail_silently=True
        )


def send_assessment_due_email(assessment, days_until_due):
    """Send assessment due reminder email"""
    subject = f"Assessment Due in {days_until_due} Days"
    message = f"""
    Dear {assessment.vendor.name},

    The following assessment is due in {days_until_due} days:
    
    Assessment: {assessment.template.name}
    Due Date: {assessment.due_date}
    Status: {assessment.get_status_display()}
    
    Please complete and submit your assessment response.

    Best regards,
    VRM System
    """
    
    # Send to vendor users
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [assessment.vendor.contact_email],
        fail_silently=True
    )
