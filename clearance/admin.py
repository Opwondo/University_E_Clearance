from time import timezone

from django.contrib import admin
from .models import (
    ClearanceWorkflow, EmailNotification, WorkflowStage, WorkflowStageDepartment,
    ClearanceSession, ClearanceRecord, ClearanceComment
)

class WorkflowStageInline(admin.TabularInline):
    model = WorkflowStage
    extra = 1

class WorkflowStageDepartmentInline(admin.TabularInline):
    model = WorkflowStageDepartment
    extra = 1

@admin.register(ClearanceWorkflow)
class ClearanceWorkflowAdmin(admin.ModelAdmin):
    list_display = ['name', 'session_type', 'is_active', 'created_at']
    list_filter = ['session_type', 'is_active']
    search_fields = ['name', 'description']
    inlines = [WorkflowStageInline]

@admin.register(WorkflowStage)
class WorkflowStageAdmin(admin.ModelAdmin):
    list_display = ['name', 'workflow', 'stage_order']
    list_filter = ['workflow']
    search_fields = ['name']
    inlines = [WorkflowStageDepartmentInline]

@admin.register(ClearanceSession)
class ClearanceSessionAdmin(admin.ModelAdmin):
    list_display = ['student', 'workflow', 'status', 'started_at', 'completed_at']
    list_filter = ['status', 'workflow', 'started_at']
    search_fields = ['student__admission_number', 'student__user__username']
    readonly_fields = ['started_at', 'last_activity']

@admin.register(ClearanceRecord)
class ClearanceRecordAdmin(admin.ModelAdmin):
    list_display = ['session', 'department', 'status', 'approved_at']
    list_filter = ['status', 'approved_at']
    search_fields = ['session__student__admission_number', 'department__name']

@admin.register(ClearanceComment)
class ClearanceCommentAdmin(admin.ModelAdmin):
    list_display = ['record', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['comment']

# ========== ADD EMAIL NOTIFICATION ADMIN ==========
@admin.register(EmailNotification)
class EmailNotificationAdmin(admin.ModelAdmin):
    """
    Admin configuration for Email Notifications
    """
    list_display = [
        'id', 
        'recipient', 
        'notification_type', 
        'subject_preview', 
        'is_sent', 
        'sent_at', 
        'created_at'
    ]
    list_filter = ['notification_type', 'is_sent', 'created_at']
    search_fields = ['recipient__email', 'recipient__username', 'subject']
    readonly_fields = ['created_at', 'sent_at', 'body_preview']
    list_editable = ['is_sent']
    
    fieldsets = (
        ('Recipient Information', {
            'fields': ('recipient', 'notification_type')
        }),
        ('Email Content', {
            'fields': ('subject', 'body', 'body_preview')
        }),
        ('Related Objects', {
            'fields': ('session', 'record'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_sent', 'sent_at', 'error_message')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def subject_preview(self, obj):
        """Show truncated subject"""
        return obj.subject[:50] + '...' if len(obj.subject) > 50 else obj.subject
    subject_preview.short_description = 'Subject'
    
    def body_preview(self, obj):
        """Show HTML preview of email body"""
        if obj.body:
            return obj.body[:200] + '...' if len(obj.body) > 200 else obj.body
        return '-'
    body_preview.short_description = 'Body Preview'
    
    actions = ['resend_selected', 'mark_as_sent', 'mark_as_failed']
    
    def resend_selected(self, request, queryset):
        """Resend selected emails"""
        from .utils.email_utils import EmailNotificationService
        
        count = 0
        for notification in queryset.filter(is_sent=False):
            EmailNotificationService.send_email_task.delay(notification.id)
            count += 1
        
        self.message_user(request, f"Rescheduled {count} email(s) for sending")
    resend_selected.short_description = "Resend selected emails"
    
    def mark_as_sent(self, request, queryset):
        """Manually mark emails as sent"""
        updated = queryset.update(is_sent=True, sent_at=timezone.now())
        self.message_user(request, f"Marked {updated} email(s) as sent")
    mark_as_sent.short_description = "Mark as sent"
    
    def mark_as_failed(self, request, queryset):
        """Manually mark emails as failed"""
        updated = queryset.update(is_sent=False, error_message="Manually marked as failed")
        self.message_user(request, f"Marked {updated} email(s) as failed")
    mark_as_failed.short_description = "Mark as failed"
# ========== END EMAIL NOTIFICATION ADMIN ==========