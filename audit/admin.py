from django.contrib import admin
from django.utils.html import format_html
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """
    Admin configuration for Audit Logs
    """
    list_display = [
        'timestamp_colored',
        'username',
        'user_role',
        'action_colored',
        'entity_info',
        'ip_address_short',
        'status_badge'
    ]
    list_filter = ['action_type', 'user_role', 'status', 'timestamp', 'entity_type']
    search_fields = ['username', 'action_description', 'entity_repr', 'ip_address']
    readonly_fields = [
        'user', 'username', 'user_role', 'action_type', 'action_description',
        'entity_type', 'entity_id', 'entity_repr', 'before_state', 'after_state',
        'ip_address', 'user_agent', 'request_method', 'request_path',
        'status', 'timestamp', 'json_before', 'json_after'
    ]
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'user_role', 'action_type', 'action_description', 'status')
        }),
        ('Entity Details', {
            'fields': ('entity_type', 'entity_id', 'entity_repr'),
            'classes': ('collapse',)
        }),
        ('State Changes', {
            'fields': ('json_before', 'json_after'),
            'classes': ('collapse',)
        }),
        ('Request Information', {
            'fields': ('ip_address', 'request_method', 'request_path', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('Timestamp', {
            'fields': ('timestamp',)
        })
    )
    
    def timestamp_colored(self, obj):
        """Color code recent logs"""
        from django.utils import timezone
        from datetime import timedelta
        
        if obj.timestamp > timezone.now() - timedelta(hours=1):
            color = 'green'
        elif obj.timestamp > timezone.now() - timedelta(hours=24):
            color = 'orange'
        else:
            color = 'gray'
            
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.timestamp.strftime('%Y-%m-%d %H:%M')
        )
    timestamp_colored.short_description = 'Timestamp'
    timestamp_colored.admin_order_field = 'timestamp'
    
    def action_colored(self, obj):
        """Color code actions by type"""
        colors = {
            'LOGIN': 'blue',
            'LOGOUT': 'gray',
            'LOGIN_FAILED': 'red',
            'CLEARANCE_APPROVED': 'green',
            'CLEARANCE_REJECTED': 'red',
            'SESSION_CREATED': 'purple',
            'USER_CREATED': 'teal',
        }
        color = colors.get(obj.action_type, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_action_type_display()
        )
    action_colored.short_description = 'Action'
    action_colored.admin_order_field = 'action_type'
    
    def entity_info(self, obj):
        """Show entity information"""
        if obj.entity_type and obj.entity_repr:
            return format_html(
                '<strong>{}</strong><br/><small>{}</small>',
                obj.entity_type,
                obj.entity_repr[:50]
            )
        return '-'
    entity_info.short_description = 'Entity'
    
    def ip_address_short(self, obj):
        """Show truncated IP address"""
        return obj.ip_address or '-'
    ip_address_short.short_description = 'IP'
    
    def status_badge(self, obj):
        """Show status as colored badge"""
        colors = {
            'SUCCESS': 'green',
            'FAILURE': 'red',
            'ERROR': 'orange',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.status
        )
    status_badge.short_description = 'Status'
    
    def json_before(self, obj):
        """Pretty print JSON before state"""
        if obj.before_state:
            import json
            return format_html('<pre>{}</pre>', json.dumps(obj.before_state, indent=2))
        return '-'
    json_before.short_description = 'Before State'
    
    def json_after(self, obj):
        """Pretty print JSON after state"""
        if obj.after_state:
            import json
            return format_html('<pre>{}</pre>', json.dumps(obj.after_state, indent=2))
        return '-'
    json_after.short_description = 'After State'
    
    actions = ['delete_selected']  # Allow deletion but with caution
    
    def has_add_permission(self, request):
        """Prevent manual addition of audit logs"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Prevent editing of audit logs"""
        return False
