from django.db import models
from django.conf import settings

class Department(models.Model):
    """
    Department model for clearance units
    """
    class DepartmentType(models.TextChoices):
        LIBRARY = 'LIBRARY', 'Library'
        FINANCE = 'FINANCE', 'Finance'
        HOSTEL = 'HOSTEL', 'Hostel'
        ICT = 'ICT', 'ICT'
        FACULTY = 'FACULTY', 'Faculty'
        SPORTS = 'SPORTS', 'Sports'
        HEALTH = 'HEALTH', 'Health Services'
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    department_type = models.CharField(
        max_length=20,
        choices=DepartmentType.choices
    )
    description = models.TextField(blank=True)
    
    # Officer in charge (can be multiple)
    officers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='managed_departments',
        limit_choices_to={'role': 'OFFICER'}
    )
    
    # Parent department (for hierarchy)
    parent_department = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sub_departments'
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'departments'
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['department_type']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def get_pending_clearances(self):
        """Get pending clearance records for this department"""
        from clearance.models import ClearanceRecord
        return ClearanceRecord.objects.filter(
            department=self,
            status='PENDING'
        ).count()
