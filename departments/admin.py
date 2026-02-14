from django.contrib import admin
from .models import Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'department_type', 'is_active', 'get_officers_count', 'created_at']
    list_filter = ['department_type', 'is_active', 'created_at']
    search_fields = ['name', 'code', 'description']
    filter_horizontal = ['officers']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'department_type', 'description')
        }),
        ('Hierarchy', {
            'fields': ('parent_department',)
        }),
        ('Officers', {
            'fields': ('officers',)
        }),
        ('Status', {
            'fields': ('is_active',)
        })
    )
    
    def get_officers_count(self, obj):
        return obj.officers.count()
    get_officers_count.short_description = 'Officers'
    
    actions = ['activate_departments', 'deactivate_departments']
    
    def activate_departments(self, request, queryset):
        queryset.update(is_active=True)
    activate_departments.short_description = "Activate selected departments"
    
    def deactivate_departments(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_departments.short_description = "Deactivate selected departments"
