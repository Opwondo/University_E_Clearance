from django.contrib import admin
from .models import (
    ClearanceWorkflow, WorkflowStage, WorkflowStageDepartment,
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
