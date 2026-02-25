from django.db import models
from django.contrib.auth import get_user_model
from .models import ClearanceSession, ClearanceRecord

User = get_user_model()

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
        User,
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
        ClearanceSession,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='email_notifications'
    )
    record = models.ForeignKey(
        ClearanceRecord,
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
