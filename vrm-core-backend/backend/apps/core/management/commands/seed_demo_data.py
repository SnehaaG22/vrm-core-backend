"""
Management command to seed demo data
Usage: python manage.py seed_demo_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User as DjangoUser
from datetime import datetime, timedelta
from django.utils import timezone
from django.apps import apps

Org = apps.get_model('core', 'Org')
User = apps.get_model('core', 'User')
Vendor = apps.get_model('core', 'Vendor')
Template = apps.get_model('core', 'Template')
Assessment = apps.get_model('core', 'Assessment')
Evidence = apps.get_model('core', 'Evidence')
Review = apps.get_model('core', 'Review')
Finding = apps.get_model('core', 'Finding')
Remediation = apps.get_model('core', 'Remediation')
AuditLog = apps.get_model('core', 'AuditLog')
Renewal = apps.get_model('core', 'Renewal')


class Command(BaseCommand):
    help = 'Seed demo data for VRM MVP'

    def handle(self, *args, **options):
        self.create_demo_data()

    def create_demo_data(self):
        """Create complete demo dataset for MVP"""
        
        print("🔄 Starting demo data seeding...")
        
        # 1. Create Organization
        print("\n📦 Creating Organization...")
        org, created = Org.objects.get_or_create(
            name='Demo Organization',
            defaults={'created_at': timezone.now()}
        )
        print(f"✓ Org: {org.name}")
        
        # 2. Create Users (Admin, Reviewer, Requester)
        print("\n👥 Creating Users...")
        users = {}
        
        # Admin User
        django_admin, created = DjangoUser.objects.get_or_create(
            username='admin@demo.com',
            defaults={
                'email': 'admin@demo.com',
                'password': 'admin123',
                'first_name': 'Admin',
                'last_name': 'User'
            }
        )
        if created:
            django_admin.set_password('admin123')
            django_admin.save()
        
        admin_user, _ = User.objects.get_or_create(
            django_user=django_admin,
            org=org,
            defaults={'role': 'admin'}
        )
        users['admin'] = admin_user
        print(f"✓ Admin: {django_admin.email}")
        
        # Reviewer User
        django_reviewer, created = DjangoUser.objects.get_or_create(
            username='reviewer@demo.com',
            defaults={
                'email': 'reviewer@demo.com',
                'password': 'reviewer123',
                'first_name': 'Reviewer',
                'last_name': 'User'
            }
        )
        if created:
            django_reviewer.set_password('reviewer123')
            django_reviewer.save()
        
        reviewer_user, _ = User.objects.get_or_create(
            django_user=django_reviewer,
            org=org,
            defaults={'role': 'reviewer'}
        )
        users['reviewer'] = reviewer_user
        print(f"✓ Reviewer: {django_reviewer.email}")
        
        # Requester User
        django_requester, created = DjangoUser.objects.get_or_create(
            username='requester@demo.com',
            defaults={
                'email': 'requester@demo.com',
                'password': 'requester123',
                'first_name': 'Requester',
                'last_name': 'User'
            }
        )
        if created:
            django_requester.set_password('requester123')
            django_requester.save()
        
        requester_user, _ = User.objects.get_or_create(
            django_user=django_requester,
            org=org,
            defaults={'role': 'requester'}
        )
        users['requester'] = requester_user
        print(f"✓ Requester: {django_requester.email}")
        
        # 3. Create Vendors
        print("\n🏢 Creating Vendors...")
        vendors = {}
        
        vendor_data = [
            {'name': 'TechCorp Solutions', 'contact_email': 'contact@techcorp.com'},
            {'name': 'CloudServices Inc', 'contact_email': 'contact@cloudservices.com'}
        ]
        
        for v_data in vendor_data:
            vendor, created = Vendor.objects.get_or_create(
                name=v_data['name'],
                org=org,
                defaults={
                    'status': 'active',
                    'contact_email': v_data['contact_email']
                }
            )
            vendors[v_data['name']] = vendor
            print(f"✓ Vendor: {vendor.name}")
        
        # Create vendor users
        print("\n👥 Creating Vendor Users...")
        for vendor in vendors.values():
            django_vendor_user, created = DjangoUser.objects.get_or_create(
                username=f"vendor_{vendor.id}@{vendor.name.lower().replace(' ', '')}",
                defaults={
                    'email': vendor.contact_email,
                    'first_name': vendor.name.split()[0],
                    'last_name': 'User'
                }
            )
            if created:
                django_vendor_user.set_password('vendor123')
                django_vendor_user.save()
            
            vendor_user, _ = User.objects.get_or_create(
                django_user=django_vendor_user,
                org=org,
                defaults={'role': 'vendor'}
            )
            print(f"✓ Vendor User: {django_vendor_user.email} for {vendor.name}")
        
        # 4. Create Template with Questions
        print("\n📋 Creating Template...")
        template, created = Template.objects.get_or_create(
            name='Security Assessment Template',
            org=org,
            version=1,
            defaults={'is_active': True}
        )
        print(f"✓ Template: {template.name} v{template.version}")
        
        # 5. Create Assessments in Different Statuses
        print("\n📊 Creating Assessments...")
        assessments = {}
        today = timezone.now()
        
        assessment_configs = [
            {
                'vendor': list(vendors.values())[0],
                'status': 'assigned',
                'due_date': today + timedelta(days=30),
                'renewal_date': today.date() + timedelta(days=365)
            },
            {
                'vendor': list(vendors.values())[0],
                'status': 'in_progress',
                'due_date': today + timedelta(days=20),
                'renewal_date': today.date() + timedelta(days=365)
            },
            {
                'vendor': list(vendors.values())[1],
                'status': 'submitted',
                'due_date': today + timedelta(days=10),
                'renewal_date': today.date() + timedelta(days=365)
            },
            {
                'vendor': list(vendors.values())[1],
                'status': 'under_review',
                'due_date': today + timedelta(days=5),
                'renewal_date': today.date() + timedelta(days=365)
            }
        ]
        
        for idx, config in enumerate(assessment_configs):
            assessment, created = Assessment.objects.get_or_create(
                vendor=config['vendor'],
                template=template,
                template_version=template.version,
                defaults={
                    'org': org,
                    'status': config['status'],
                    'assigned_by': users['admin'],
                    'due_date': config['due_date'],
                    'renewal_date': config['renewal_date']
                }
            )
            assessments[idx] = assessment
            print(f"✓ Assessment {idx+1}: {assessment.vendor.name} - Status: {assessment.get_status_display()}")
        
        # 6. Create Evidence
        print("\n📄 Creating Evidence...")
        evidence_items = []
        
        for idx, assessment in assessments.items():
            if idx < 2:  # Add evidence to first 2 assessments
                evidence, created = Evidence.objects.get_or_create(
                    assessment=assessment,
                    file_name=f"security_report_{assessment.id}.pdf",
                    defaults={
                        'file_type': 'document',
                        'file_path': f"/evidence/reports/security_report_{assessment.id}.pdf",
                        'file_size': 1024000,
                        'uploaded_by': users['requester'],
                        'expiry_date': today.date() + timedelta(days=180),
                        'is_expired': False
                    }
                )
                evidence_items.append(evidence)
                print(f"✓ Evidence: {evidence.file_name} (expires: {evidence.expiry_date})")
        
        # 7. Create Review for submitted assessment
        print("\n🔍 Creating Review...")
        if assessments[2].status == 'submitted':
            review, created = Review.objects.get_or_create(
                assessment=assessments[2],
                defaults={
                    'reviewed_by': users['reviewer'],
                    'status': 'pending',
                    'comments': 'Assessment received. Under review.'
                }
            )
            print(f"✓ Review: {review.assessment.vendor.name}")
        
        # 8. Create Finding and Remediation
        print("\n⚠️ Creating Findings & Remediation...")
        if assessments[2]:
            finding, created = Finding.objects.get_or_create(
                assessment=assessments[2],
                defaults={
                    'description': 'Weak password policy detected in user management system',
                    'severity': 'high'
                }
            )
            print(f"✓ Finding: {finding.severity.upper()} - {finding.description[:50]}...")
            
            remediation, created = Remediation.objects.get_or_create(
                finding=finding,
                defaults={
                    'requested_by': users['reviewer'],
                    'status': 'requested',
                    'due_date': today.date() + timedelta(days=30),
                    'vendor_response': None
                }
            )
            print(f"✓ Remediation: Status - {remediation.get_status_display()}")
        
        # 9. Create Renewal
        print("\n🔄 Creating Renewal...")
        if assessments[0]:
            renewal, created = Renewal.objects.get_or_create(
                assessment=assessments[0],
                defaults={
                    'status': 'pending',
                    'due_date': today.date() + timedelta(days=365)
                }
            )
            print(f"✓ Renewal: {renewal.assessment.vendor.name} (due: {renewal.due_date})")
        
        # 10. Create Sample Audit Logs
        print("\n📝 Creating Audit Logs...")
        AuditLog.objects.create(
            org=org,
            actor=users['admin'],
            action='create',
            entity_type='assessment',
            entity_id=assessments[0].id,
            changes={'status': assessments[0].status}
        )
        
        print("✓ Audit logs created")
        
        # Print Summary
        print("\n" + "="*50)
        print("✅ DEMO DATA SEEDING COMPLETE!")
        print("="*50)
        print("\n📌 TEST CREDENTIALS:\n")
        print("Admin User:")
        print("  Email: admin@demo.com")
        print("  Password: admin123")
        print("\nReviewer User:")
        print("  Email: reviewer@demo.com")
        print("  Password: reviewer123")
        print("\nRequester User:")
        print("  Email: requester@demo.com")
        print("  Password: requester123")
        print("\nVendor User (TechCorp):")
        print("  Email: contact@techcorp.com")
        print("  Password: vendor123")
        print("\n" + "="*50)
        print("\n📊 SUMMARY:")
        print(f"Organizations: 1")
        print(f"Users: 3 (Admin, Reviewer, Requester) + 2 Vendor Users")
        print(f"Vendors: 2")
        print(f"Templates: 1")
        print(f"Assessments: 4 (various statuses)")
        print(f"Evidence Items: 2")
        print(f"Findings: 1")
        print(f"Remediations: 1")
        print(f"Renewals: 1")
        print("="*50 + "\n")
