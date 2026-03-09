from django.db import models
from django.conf import settings

class StudentProfile(models.Model):
    """
    Student profile model extending the User model
    """
    class YearOfStudy(models.TextChoices):
        YEAR_1 = 'Y1', 'Year 1'
        YEAR_2 = 'Y2', 'Year 2'
        YEAR_3 = 'Y3', 'Year 3'
        YEAR_4 = 'Y4', 'Year 4'
        YEAR_5 = 'Y5', 'Year 5'
        GRADUATED = 'GRAD', 'Graduated'
    
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        GRADUATED = 'GRADUATED', 'Graduated'
        WITHDRAWN = 'WITHDRAWN', 'Withdrawn'
        SUSPENDED = 'SUSPENDED', 'Suspended'
    
    # Link to User model (One-to-One)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    
    # Student-specific fields
    admission_number = models.CharField(max_length=20, unique=True)
    registration_number = models.CharField(max_length=20, unique=True)
    
    # Academic information
    faculty = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    year_of_study = models.CharField(
        max_length=10,
        choices=YearOfStudy.choices,
        default=YearOfStudy.YEAR_1
    )
    
    # Personal information
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'student_profiles'
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'
        indexes = [
            models.Index(fields=['admission_number']),
            models.Index(fields=['registration_number']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.admission_number} - {self.user.get_full_name() or self.user.username}"
    
    # ⬇️ THIS METHOD MUST BE INDENTED INSIDE THE CLASS ⬇️
    def get_clearance_status(self):
        """
        Get overall clearance status for this student
        """
        try:
            from clearance.models import ClearanceRecord
            # Fix: Use session__student instead of student
            records = ClearanceRecord.objects.filter(session__student=self)
            if not records.exists():
                return 'NOT_STARTED'
            if records.filter(status='REJECTED').exists():
                return 'REJECTED'
            if records.filter(status='PENDING').exists():
                return 'IN_PROGRESS'
            if records.filter(status='APPROVED').count() == records.count():
                return 'CLEARED'
            return 'IN_PROGRESS'
        except Exception as e:
            print(f"Error in get_clearance_status: {e}")
            return 'NOT_STARTED'