from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User Model for the E-Clearance System
    """
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        OFFICER = 'OFFICER', 'Department Officer'
        ADMIN = 'ADMIN', 'Administrator'
    
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.STUDENT,
        help_text="User role in the system"
    )
    
    # Additional fields
    phone_number = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.username} - {self.role}"
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
