from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import json

User = get_user_model()

class AuditLog(models.Model):
    """
    Track all important actions in the system
    """
    class ActionType(models.TextChoices):
        # Authentication actions
        LOGIN = 'LOGIN', 'User Login'
        LOGOUT = 'LOGOUT', 'User Logout'
        LOGIN_FAILED = 'LOGIN_FAILED', 'Failed Login Attempt'
        
        # User management
        USER_CREATED = 'USER_CREATED', 'User Created'
        USER_UPDATED = 'USER_UPDATED', 'User Updated'
        USER_DELETED = 'USER_DELETED', 'User Deleted'
        
        # Clearance actions
        CLEARANCE_SESSION_CREATED = 'SESSION_CREATED', 'Clearance Session Created'
        CLEARANCE_APPROVED = 'CLEARANCE_APPROVED', 'Clearance Approved'
        CLEARANCE_REJECTED = 'CLEARANCE_REJECTED', 'Clearance Rejected'
        CLEARANCE_COMPLETED = 'CLEARANCE_COMPLETED', 'Clearance Completed'
        
        # Department actions
        DEPARTMENT_CREATED = 'DEPT_CREATED', 'Department Created'
        DEPARTMENT_UPDATED = 'DEPT_UPDATED', 'Department Updated'
        DEPARTMENT_DELETED = 'DEPT_DELETED', 'Department Deleted'
        OFFICER_ASSIGNED = 'OFFICER_ASSIGNED', 'Officer Assigned'
        OFFICER_REMOVED = 'OFFICER_REMOVED', 'Officer Removed'
        
        # Student actions
        STUDENT_CREATED = 'STUDENT_CREATED', 'Student Profile Created'
        STUDENT_UPDATED = 'STUDENT_UPDATED', 'Student Profile Updated'
        STUDENT_DELETED = 'STUDENT_DELETED', 'Student Profile Deleted'
    
    # Who performed the action
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    username = models.CharField(max_length=150, blank=True)  # Store username in case user is deleted
    user_role = models.CharField(max_length=20, blank=True)  # Store user role at time of action
    
    # What action was performed
    action_type = models.CharField(
        max_length=30,
        choices=ActionType.choices
    )
    action_description = models.TextField()
    
    # What was affected
    entity_type = models.CharField(max_length=50)  # e.g., 'ClearanceSession', 'User', 'Department'
    entity_id = models.IntegerField(null=True, blank=True)
    entity_repr = models.CharField(max_length=255, blank=True)  # String representation of the entity
    
    # Before and after state (for updates)
    before_state = models.JSONField(null=True, blank=True)
    after_state = models.JSONField(null=True, blank=True)
    
    # Request information
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    request_method = models.CharField(max_length=10, blank=True)
    request_path = models.CharField(max_length=255, blank=True)
    
    # Status
    status = models.CharField(max_length=20, default='SUCCESS')  # SUCCESS, FAILURE, ERROR
    
    # Timestamp
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    
    class Meta:
        db_table = 'audit_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action_type', '-timestamp']),
            models.Index(fields=['entity_type', 'entity_id']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M')} - {self.get_action_type_display()} by {self.username or 'System'}"
    
    def save(self, *args, **kwargs):
        # Store username and role if user exists
        if self.user and not self.username:
            self.username = self.user.username
            self.user_role = self.user.role
        super().save(*args, **kwargs)
    
    @classmethod
    def log_action(cls, user, action_type, description, entity=None, request=None, **kwargs):
        """
        Helper method to create audit log entries
        """
        log_entry = cls(
            user=user,
            username=user.username if user else 'System',
            user_role=user.role if user else 'SYSTEM',
            action_type=action_type,
            action_description=description,
            **kwargs
        )
        
        # Add entity information if provided
        if entity:
            log_entry.entity_type = entity.__class__.__name__
            log_entry.entity_id = entity.id
            log_entry.entity_repr = str(entity)
        
        # Add request information if provided
        if request:
            log_entry.ip_address = cls._get_client_ip(request)
            log_entry.user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
            log_entry.request_method = request.method
            log_entry.request_path = request.path
        
        log_entry.save()
        return log_entry
    
    @staticmethod
    def _get_client_ip(request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
