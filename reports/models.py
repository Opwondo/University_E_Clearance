from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class ClearanceStatistics(models.Model):
    """
    Store aggregated clearance statistics for faster retrieval
    """
    date = models.DateField(unique=True)
    
    # Overview stats
    total_sessions = models.IntegerField(default=0)
    completed_sessions = models.IntegerField(default=0)
    in_progress_sessions = models.IntegerField(default=0)
    blocked_sessions = models.IntegerField(default=0)
    
    # Time-based stats
    avg_completion_days = models.FloatField(default=0.0)
    fastest_completion_days = models.FloatField(default=0.0)
    slowest_completion_days = models.FloatField(default=0.0)
    
    # Department stats
    total_departments = models.IntegerField(default=0)
    active_departments = models.IntegerField(default=0)
    
    # Student stats
    total_students = models.IntegerField(default=0)
    students_with_clearance = models.IntegerField(default=0)
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reports_statistics'
        ordering = ['-date']
    
    def __str__(self):
        return f"Statistics for {self.date}"

class DepartmentPerformance(models.Model):
    """
    Track performance metrics for each department
    """
    department = models.ForeignKey(
        'departments.Department',
        on_delete=models.CASCADE,
        related_name='performance_metrics'
    )
    date = models.DateField()
    
    # Volume metrics
    total_requests = models.IntegerField(default=0)
    pending_requests = models.IntegerField(default=0)
    approved_requests = models.IntegerField(default=0)
    rejected_requests = models.IntegerField(default=0)
    
    # Time metrics
    avg_response_days = models.FloatField(default=0.0)
    avg_response_hours = models.FloatField(default=0.0)
    fastest_response_hours = models.FloatField(default=0.0)
    slowest_response_hours = models.FloatField(default=0.0)
    
    # Rate metrics
    approval_rate = models.FloatField(default=0.0)  # Percentage
    rejection_rate = models.FloatField(default=0.0)
    
    class Meta:
        db_table = 'reports_department_performance'
        ordering = ['-date', 'department']
        unique_together = ['department', 'date']
    
    def __str__(self):
        return f"{self.department.name} - {self.date}"

class StudentProgress(models.Model):
    """
    Track individual student progress
    """
    student = models.ForeignKey(
        'students.StudentProfile',
        on_delete=models.CASCADE,
        related_name='progress_tracking'
    )
    session = models.ForeignKey(
        'clearance.ClearanceSession',
        on_delete=models.CASCADE,
        related_name='progress'
    )
    
    # Progress metrics
    departments_completed = models.IntegerField(default=0)
    total_departments = models.IntegerField(default=0)
    progress_percentage = models.FloatField(default=0.0)
    
    # Time tracking
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    days_to_complete = models.FloatField(null=True, blank=True)
    
    # Status
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'reports_student_progress'
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.student.user.username} - {self.progress_percentage}%"
