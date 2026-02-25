from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .utils import AuditLogger

User = get_user_model()

@receiver(post_save, sender=User)
def log_user_changes(sender, instance, created, **kwargs):
    """Log user creation and updates"""
    action = 'create' if created else 'update'
    AuditLogger.log_entity_changes(action, instance)

@receiver(pre_delete, sender=User)
def log_user_deletion(sender, instance, **kwargs):
    """Log user deletion"""
    AuditLogger.log_entity_changes('delete', instance)

# Add similar signals for other models as needed
