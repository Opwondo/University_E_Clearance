import threading
from django.utils import timezone
from .models import AuditLog

# Thread-local storage for current request
_thread_locals = threading.local()

def get_current_request():
    """Get the current request from thread-local storage"""
    return getattr(_thread_locals, 'request', None)

class AuditLogMiddleware:
    """
    Middleware to capture request information for audit logs
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Store request in thread-local storage
        _thread_locals.request = request
        
        # Process the request
        response = self.get_response(request)
        
        # Clean up
        if hasattr(_thread_locals, 'request'):
            del _thread_locals.request
        
        return response
    
    def process_exception(self, request, exception):
        """Log exceptions"""
        from .models import AuditLog
        
        AuditLog.log_action(
            user=getattr(request, 'user', None),
            action_type='ERROR',
            description=f"Exception: {str(exception)[:200]}",
            request=request,
            status='ERROR',
            entity_type='Exception',
            after_state={'error': str(exception)}
        )
        return None
