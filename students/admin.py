from django.contrib import admin
from django.utils.html import format_html
from .models import StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = [
        'admission_number', 
        'user', 
        'faculty', 
        'department', 
        'year_of_study', 
        'status',
        'clearance_status_display' 
    ]
    list_filter = ['faculty', 'department', 'year_of_study', 'status']
    search_fields = [
        'admission_number', 
        'registration_number', 
        'user__username', 
        'user__email'
    ]
    raw_id_fields = ['user']
    readonly_fields = ['created_at', 'updated_at', 'clearance_status_display']
    
    fieldsets = (
        ('User Account', {
            'fields': ('user',)
        }),
        ('Student Identification', {
            'fields': ('admission_number', 'registration_number')
        }),
        ('Academic Information', {
            'fields': ('faculty', 'department', 'course', 'year_of_study')
        }),
        ('Personal Information', {
            'fields': ('date_of_birth', 'address', 'phone_number'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status', 'clearance_status_display')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def clearance_status_display(self, obj):
        """Display clearance status with colors"""
        try:
            # Fix: Use session__student instead of student
            from clearance.models import ClearanceRecord
            records = ClearanceRecord.objects.filter(session__student=obj)
            
            if not records.exists():
                status_text = 'NOT_STARTED'
                color = 'orange'
            elif records.filter(status='REJECTED').exists():
                status_text = 'REJECTED'
                color = 'red'
            elif records.filter(status='PENDING').exists():
                status_text = 'IN_PROGRESS'
                color = 'blue'
            elif records.filter(status='APPROVED').count() == records.count():
                status_text = 'CLEARED'
                color = 'green'
            else:
                status_text = 'IN_PROGRESS'
                color = 'blue'
            
            return format_html(
                '<span style="color: {}; font-weight: bold;">{}</span>',
                color,
                status_text
            )
        except Exception as e:
            return format_html(
                '<span style="color: gray;">Error: {}</span>',
                str(e)
            )
    
    clearance_status_display.short_description = 'Clearance Status'
    
    actions = ['activate_selected', 'deactivate_selected']
    
    def activate_selected(self, request, queryset):
        queryset.update(status='ACTIVE')
    activate_selected.short_description = "Activate selected students"
    
    def deactivate_selected(self, request, queryset):
        queryset.update(status='WITHDRAWN')
    deactivate_selected.short_description = "Deactivate selected students"