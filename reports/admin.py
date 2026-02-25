from django.contrib import admin
from .models import ClearanceStatistics, DepartmentPerformance, StudentProgress

@admin.register(ClearanceStatistics)
class ClearanceStatisticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_sessions', 'completed_sessions', 'avg_completion_days']
    list_filter = ['date']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(DepartmentPerformance)
class DepartmentPerformanceAdmin(admin.ModelAdmin):
    list_display = ['department', 'date', 'total_requests', 'approval_rate']
    list_filter = ['date', 'department']
    
    def approval_rate(self, obj):
        return f"{obj.approval_rate}%"

@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'progress_percentage', 'is_completed', 'started_at']
    list_filter = ['is_completed', 'started_at']
