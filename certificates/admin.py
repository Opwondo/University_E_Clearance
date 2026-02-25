from django.contrib import admin
from .models import CertificateTemplate, GeneratedCertificate

@admin.register(CertificateTemplate)
class CertificateTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_type', 'is_active', 'created_at']
    list_filter = ['template_type', 'is_active']
    search_fields = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'template_type', 'is_active')
        }),
        ('Files', {
            'fields': ('template_file', 'background_image')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ['created_at', 'updated_at']

@admin.register(GeneratedCertificate)
class GeneratedCertificateAdmin(admin.ModelAdmin):
    list_display = [
        'certificate_number', 'student', 'session',
        'issue_date', 'download_count', 'is_verified'
    ]
    list_filter = ['is_verified', 'issue_date']
    search_fields = ['certificate_number', 'student__user__username']
    readonly_fields = [
        'certificate_number', 'verification_code', 'issue_date',
        'download_count', 'last_downloaded', 'verified_at'
    ]
    
    fieldsets = (
        ('Certificate Information', {
            'fields': ('certificate_number', 'verification_code', 'issue_date')
        }),
        ('Related Objects', {
            'fields': ('session', 'student')
        }),
        ('File', {
            'fields': ('pdf_file',)
        }),
        ('Verification', {
            'fields': ('is_verified', 'verified_at', 'verified_by')
        }),
        ('Downloads', {
            'fields': ('download_count', 'last_downloaded')
        })
    )
    
    actions = ['mark_as_verified', 'reset_verification']
    
    def mark_as_verified(self, request, queryset):
        updated = queryset.update(
            is_verified=True,
            verified_at=timezone.now(),
            verified_by=request.user
        )
        self.message_user(request, f"{updated} certificates marked as verified")
    mark_as_verified.short_description = "Mark selected as verified"
    
    def reset_verification(self, request, queryset):
        updated = queryset.update(is_verified=False, verified_at=None, verified_by=None)
        self.message_user(request, f"{updated} certificates verification reset")
    reset_verification.short_description = "Reset verification status"
