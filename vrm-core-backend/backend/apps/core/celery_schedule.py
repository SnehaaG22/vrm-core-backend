"""
Celery Beat Schedule Configuration for Periodic Tasks
"""

from celery.schedules import crontab

# Celery Beat Schedule
CELERY_BEAT_SCHEDULE = {
    # Daily task: Mark expired evidence
    'mark-expired-evidence': {
        'task': 'backend.apps.core.tasks.mark_expired_evidence',
        'schedule': crontab(hour=0, minute=0),  # Every day at midnight
        'options': {'queue': 'default'}
    },
    
    # Daily task: Send evidence expiry reminders (30, 15, 7 days)
    'evidence-expiry-reminder': {
        'task': 'backend.apps.core.tasks.evidence_expiry_reminder',
        'schedule': crontab(hour=8, minute=0),  # Every day at 8 AM
        'options': {'queue': 'default'}
    },
    
    # Daily task: Send renewal reminders
    'renewal-due-reminder': {
        'task': 'backend.apps.core.tasks.renewal_due_reminder',
        'schedule': crontab(hour=9, minute=0),  # Every day at 9 AM
        'options': {'queue': 'default'}
    },
    
    # Weekly task: Send assessment due reminders
    'assessment-due-reminder': {
        'task': 'backend.apps.core.tasks.assessment_due_reminder',
        'schedule': crontab(hour=10, minute=0, day_of_week=1),  # Every Monday at 10 AM
        'options': {'queue': 'default'}
    },
}
