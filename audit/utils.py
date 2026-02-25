from .models import AuditLog
from .middleware import get_current_request
from django.contrib.auth import get_user_model

User = get_user_model()

class AuditLogger:
    """
    Utility class for creating audit logs
    """
    
    @classmethod
    def log(cls, action_type, description, entity=None, user=None, 
            before_state=None, after_state=None, status='SUCCESS'):
        """
        Create an audit log entry
        """
        request = get_current_request()
        
        # Get user from request if not provided
        if not user and request and hasattr(request, 'user'):
            user = request.user if request.user.is_authenticated else None
        
        # Create the log entry
        return AuditLog.log_action(
            user=user,
            action_type=action_type,
            description=description,
            entity=entity,
            request=request,
            before_state=before_state,
            after_state=after_state,
            status=status
        )
    
    @classmethod
    def log_login(cls, user, success=True, request=None):
        """Log login attempts"""
        action = 'LOGIN' if success else 'LOGIN_FAILED'
        description = f"User {user.username} logged in successfully" if success else f"Failed login attempt for {user.username}"
        return cls.log(action, description, user=user, status='SUCCESS' if success else 'FAILURE')
    
    @classmethod
    def log_logout(cls, user, request=None):
        """Log logout"""
        return cls.log('LOGOUT', f"User {user.username} logged out", user=user)
    
    @classmethod
    def log_clearance_action(cls, action, record, user=None, remarks=None):
        """Log clearance approvals/rejections"""
        action_map = {
            'approve': 'CLEARANCE_APPROVED',
            'reject': 'CLEARANCE_REJECTED',
        }
        
        action_type = action_map.get(action)
        if not action_type:
            return None
        
        description = f"Clearance {action}ed for {record.session.student.user.username} by {record.department.name}"
        if remarks:
            description += f" - Remarks: {remarks}"
        
        return cls.log(
            action_type=action_type,
            description=description,
            entity=record,
            user=user,
            after_state={'status': action.upper(), 'remarks': remarks}
        )
    
    @classmethod
    def log_entity_changes(cls, action, entity, user=None, changes=None):
        """Log entity changes (create, update, delete)"""
        action_map = {
            'create': f"{entity.__class__.__name__.upper()}_CREATED",
            'update': f"{entity.__class__.__name__.upper()}_UPDATED",
            'delete': f"{entity.__class__.__name__.upper()}_DELETED",
        }
        
        action_type = action_map.get(action)
        if not action_type:
            return None
        
        description = f"{action.title()}d {entity.__class__.__name__}: {entity}"
        
        return cls.log(
            action_type=action_type,
            description=description,
            entity=entity,
            user=user,
            after_state=changes if action == 'create' else None,
            before_state=changes if action == 'update' else None
        )
    
    @classmethod
    def get_user_logs(cls, user, limit=50):
        """Get audit logs for a specific user"""
        return AuditLog.objects.filter(user=user)[:limit]
    
    @classmethod
    def get_entity_logs(cls, entity, limit=50):
        """Get audit logs for a specific entity"""
        return AuditLog.objects.filter(
            entity_type=entity.__class__.__name__,
            entity_id=entity.id
        )[:limit]
    
    @classmethod
    def get_recent_activities(cls, limit=100):
        """Get recent activities across the system"""
        return AuditLog.objects.all()[:limit]
