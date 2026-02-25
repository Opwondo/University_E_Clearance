from django.db import models
from django.contrib.auth import get_user_model
from students.models import StudentProfile
from departments.models import Department

User = get_user_model()

class ClearanceWorkflow(models.Model):
    """
    Defines different clearance workflows (Graduation, Transfer, Internship, etc.)
    """
    class SessionType(models.TextChoices):
        GRADUATION = 'GRADUATION', 'Graduation Clearance'
        TRANSFER = 'TRANSFER', 'Transfer Clearance'
        INTERNSHIP = 'INTERNSHIP', 'Internship Clearance'
        WITHDRAWAL = 'WITHDRAWAL', 'Student Withdrawal'
    
    name = models.CharField(max_length=100)
    session_type = models.CharField(
        max_length=20,
        choices=SessionType.choices,
        unique=True
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'clearance_workflows'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_session_type_display()})"

class WorkflowStage(models.Model):
    """
    Represents a stage in the clearance workflow (e.g., Academic Clearance)
    """
    workflow = models.ForeignKey(
        ClearanceWorkflow, 
        on_delete=models.CASCADE,
        related_name='stages'
    )
    name = models.CharField(max_length=100)  # e.g., "Academic Clearance"
    stage_order = models.PositiveIntegerField()  # 1, 2, 3, etc.
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = 'workflow_stages'
        ordering = ['workflow', 'stage_order']
        unique_together = ['workflow', 'stage_order']
    
    def __str__(self):
        return f"{self.workflow.name} - Stage {self.stage_order}: {self.name}"

class WorkflowStageDepartment(models.Model):
    """
    Departments that must be cleared within a stage (can be parallel)
    """
    stage = models.ForeignKey(
        WorkflowStage,
        on_delete=models.CASCADE,
        related_name='departments'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='workflow_stages'
    )
    order_within_stage = models.PositiveIntegerField(
        default=0,
        help_text="Order within stage (0 means can be done in parallel)"
    )
    is_mandatory = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'workflow_stage_departments'
        ordering = ['stage', 'order_within_stage']
        unique_together = ['stage', 'department']
    
    def __str__(self):
        return f"{self.stage.name} - {self.department.name}"

class ClearanceSession(models.Model):
    """
    A student's clearance session
    """
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Not Started'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        BLOCKED = 'BLOCKED', 'Blocked'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
    
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='clearance_sessions'
    )
    workflow = models.ForeignKey(
        ClearanceWorkflow,
        on_delete=models.PROTECT,
        related_name='sessions'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    current_stage = models.ForeignKey(
        WorkflowStage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='active_sessions'
    )
    
    # Tracking
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    # Metadata
    remarks = models.TextField(blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_clearance_sessions'
    )
    
    class Meta:
        db_table = 'clearance_sessions'
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['status', 'current_stage']),
        ]
    
    def __str__(self):
        return f"{self.student.admission_number} - {self.workflow.name} ({self.get_status_display()})"
    
    def get_progress_percentage(self):
        """Calculate overall clearance progress"""
        total_depts = WorkflowStageDepartment.objects.filter(
            stage__workflow=self.workflow
        ).count()
        
        approved_depts = self.records.filter(status='APPROVED').count()
        
        if total_depts == 0:
            return 0
        
        return int((approved_depts / total_depts) * 100)
    
    def get_current_stage_progress(self):
        """Get progress within current stage"""
        if not self.current_stage:
            return 0
        
        stage_depts = WorkflowStageDepartment.objects.filter(stage=self.current_stage)
        total_in_stage = stage_depts.count()
        
        if total_in_stage == 0:
            return 100
        
        approved_in_stage = self.records.filter(
            department__in=[d.department for d in stage_depts],
            status='APPROVED'
        ).count()
        
        return int((approved_in_stage / total_in_stage) * 100)

class ClearanceRecord(models.Model):
    """
    Individual department clearance record
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        WAIVED = 'WAIVED', 'Waived (Not Required)'
    
    session = models.ForeignKey(
        ClearanceSession,
        on_delete=models.CASCADE,
        related_name='records'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name='clearance_records'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    
    # Approval details
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_clearances'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    
    # Rejection details
    remarks = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'clearance_records'
        ordering = ['department__name']
        unique_together = ['session', 'department']  # One record per department per session
    
    def __str__(self):
        return f"{self.session.student.admission_number} - {self.department.name}: {self.status}"
    
    def can_approve(self):
        """Check if this record can be approved"""
        # Can't approve if already approved
        if self.status == 'APPROVED':
            return False
        
        # Check if session is in progress
        if self.session.status != 'IN_PROGRESS':
            return False
        
        # Get the stage for this department
        try:
            stage_dept = WorkflowStageDepartment.objects.get(
                department=self.department,
                stage__workflow=self.session.workflow
            )
            stage = stage_dept.stage
        except WorkflowStageDepartment.DoesNotExist:
            return False
        
        # Check if previous stages are completed
        previous_stages = WorkflowStage.objects.filter(
            workflow=self.session.workflow,
            stage_order__lt=stage.stage_order
        )
        
        for prev_stage in previous_stages:
            stage_depts = WorkflowStageDepartment.objects.filter(stage=prev_stage)
            approved_in_prev = ClearanceRecord.objects.filter(
                session=self.session,
                department__in=[d.department for d in stage_depts],
                status='APPROVED'
            ).count()
            
            if approved_in_prev < stage_depts.count():
                return False
        
        return True

class ClearanceComment(models.Model):
    """
    Comments on clearance records (especially for rejections)
    """
    record = models.ForeignKey(
        ClearanceRecord,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='clearance_comments'
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'clearance_comments'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment on {self.record} by {self.author}"

# ========== EMAIL NOTIFICATION MODEL - BEGIN ==========
class EmailNotification(models.Model):
    """
    Track email notifications sent by the system
    """
    class NotificationType(models.TextChoices):
        SESSION_CREATED = 'SESSION_CREATED', 'Clearance Session Created'
        RECORD_APPROVED = 'RECORD_APPROVED', 'Department Approved'
        RECORD_REJECTED = 'RECORD_REJECTED', 'Department Rejected'
        SESSION_COMPLETED = 'SESSION_COMPLETED', 'Clearance Completed'
        PENDING_REMINDER = 'PENDING_REMINDER', 'Pending Clearance Reminder'
    
    recipient = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='email_notifications'
    )
    notification_type = models.CharField(
        max_length=30,
        choices=NotificationType.choices
    )
    subject = models.CharField(max_length=255)
    body = models.TextField()
    
    # Related objects (optional)
    session = models.ForeignKey(
        'clearance.ClearanceSession',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='email_notifications'
    )
    record = models.ForeignKey(
        'clearance.ClearanceRecord',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='email_notifications'
    )
    
    # Status tracking
    sent_at = models.DateTimeField(null=True, blank=True)
    is_sent = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'email_notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['is_sent']),
        ]
    
    def __str__(self):
        return f"{self.get_notification_type_display()} to {self.recipient.email} - {'✅' if self.is_sent else '❌'}"
# ========== EMAIL NOTIFICATION MODEL - END ==========
