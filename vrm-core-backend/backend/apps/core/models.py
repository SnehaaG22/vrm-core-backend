from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User as DjangoUser


class Org(models.Model):
    """Organization/Tenant model"""
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class User(models.Model):
    """Custom User model with role-based access"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('reviewer', 'Reviewer'),
        ('requester', 'Requester'),
        ('vendor', 'Vendor'),
    ]

    django_user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    org = models.ForeignKey(Org, on_delete=models.CASCADE, related_name='users')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.django_user.username} ({self.role})"

    class Meta:
        ordering = ['-created_at']
        unique_together = ('django_user', 'org')


class Vendor(models.Model):
    """Vendor/Third-party model"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]

    name = models.CharField(max_length=255)
    org = models.ForeignKey(Org, on_delete=models.CASCADE, related_name='vendors')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    contact_email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        unique_together = ('name', 'org')


class Template(models.Model):
    """Assessment Template with versioning"""
    name = models.CharField(max_length=255)
    org = models.ForeignKey(Org, on_delete=models.CASCADE, related_name='templates')
    version = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} v{self.version}"

    class Meta:
        ordering = ['-created_at']
        unique_together = ('name', 'org', 'version')


class Assessment(models.Model):
    """Assessment instance"""
    STATUS_CHOICES = [
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('remediation', 'Remediation'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    org = models.ForeignKey(Org, on_delete=models.CASCADE, related_name='assessments')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='assessments')
    template = models.ForeignKey(Template, on_delete=models.PROTECT)
    template_version = models.IntegerField()  # Locked at assignment time
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='assigned')
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_assessments')
    assigned_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    renewal_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vendor.name} - {self.template.name}"

    class Meta:
        ordering = ['-created_at']
        unique_together = ('vendor', 'template', 'template_version')


class Evidence(models.Model):
    """Evidence files attached to assessments/responses"""
    FILE_TYPE_CHOICES = [
        ('document', 'Document'),
        ('image', 'Image'),
        ('spreadsheet', 'Spreadsheet'),
        ('video', 'Video'),
        ('other', 'Other'),
    ]

    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='evidences')
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50, choices=FILE_TYPE_CHOICES)
    file_path = models.CharField(max_length=500)  # MinIO path
    file_size = models.BigIntegerField()
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField()
    is_expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name

    class Meta:
        ordering = ['-uploaded_at']


class Review(models.Model):
    """Assessment Review"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('remediation_requested', 'Remediation Requested'),
    ]

    assessment = models.OneToOneField(Assessment, on_delete=models.CASCADE, related_name='review')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    comments = models.TextField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review: {self.assessment.vendor.name}"

    class Meta:
        ordering = ['-created_at']


class Finding(models.Model):
    """Finding from assessment review"""
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='findings')
    description = models.TextField()
    severity = models.CharField(max_length=50, choices=SEVERITY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.severity.upper()}: {self.description[:50]}"

    class Meta:
        ordering = ['-created_at']


class Remediation(models.Model):
    """Remediation request"""
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('verified', 'Verified'),
        ('closed', 'Closed'),
    ]

    finding = models.OneToOneField(Finding, on_delete=models.CASCADE, related_name='remediation')
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='requested')
    due_date = models.DateField()
    vendor_response = models.TextField(null=True, blank=True)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_remediations')
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Remediation: {self.finding.description[:50]}"

    class Meta:
        ordering = ['-created_at']


class AuditLog(models.Model):
    """Audit log for all critical actions"""
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('submit', 'Submit'),
        ('review', 'Review'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('remediation_request', 'Remediation Request'),
        ('remediation_submit', 'Remediation Submit'),
        ('remediation_close', 'Remediation Close'),
        ('renewal_trigger', 'Renewal Trigger'),
    ]

    ENTITY_TYPE_CHOICES = [
        ('assessment', 'Assessment'),
        ('evidence', 'Evidence'),
        ('review', 'Review'),
        ('finding', 'Finding'),
        ('remediation', 'Remediation'),
        ('vendor', 'Vendor'),
        ('template', 'Template'),
        ('user', 'User'),
    ]

    org = models.ForeignKey(Org, on_delete=models.CASCADE, related_name='audit_logs')
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    entity_type = models.CharField(max_length=50, choices=ENTITY_TYPE_CHOICES)
    entity_id = models.IntegerField()
    changes = models.JSONField(null=True, blank=True)  # Store what changed
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} {self.entity_type}: {self.entity_id}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['org', 'created_at']),
            models.Index(fields=['entity_type', 'entity_id']),
        ]


class Renewal(models.Model):
    """Renewal tracking for assessments"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('triggered', 'Triggered'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
    ]

    assessment = models.OneToOneField(Assessment, on_delete=models.CASCADE, related_name='renewal')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateField()
    triggered_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Renewal: {self.assessment.vendor.name}"

    class Meta:
        ordering = ['-created_at']
