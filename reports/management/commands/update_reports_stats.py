from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Count, Avg, Q
from datetime import timedelta
from reports.models import ClearanceStatistics, DepartmentPerformance
from clearance.models import ClearanceSession, ClearanceRecord
from departments.models import Department

class Command(BaseCommand):
    help = 'Update daily report statistics'
    
    def handle(self, *args, **options):
        self.stdout.write('Updating report statistics...')
        
        today = timezone.now().date()
        
        # Update clearance statistics
        stats, created = ClearanceStatistics.objects.get_or_create(date=today)
        
        sessions = ClearanceSession.objects.filter(started_at__date=today)
        stats.total_sessions = sessions.count()
        stats.completed_sessions = sessions.filter(status='COMPLETED').count()
        stats.in_progress_sessions = sessions.filter(status='IN_PROGRESS').count()
        stats.blocked_sessions = sessions.filter(status='BLOCKED').count()
        
        # Calculate average completion time
        completed = sessions.filter(status='COMPLETED', completed_at__isnull=False)
        total_days = 0
        count = 0
        
        for session in completed:
            if session.completed_at and session.started_at:
                delta = session.completed_at - session.started_at
                days = delta.total_seconds() / 86400
                total_days += days
                count += 1
        
        stats.avg_completion_days = total_days / count if count > 0 else 0
        
        # Department stats
        stats.total_departments = Department.objects.filter(is_active=True).count()
        
        # Student stats
        from students.models import StudentProfile
        stats.total_students = StudentProfile.objects.count()
        
        stats.save()
        
        # Update department performance
        for dept in Department.objects.filter(is_active=True):
            perf, created = DepartmentPerformance.objects.get_or_create(
                department=dept,
                date=today
            )
            
            records = ClearanceRecord.objects.filter(department=dept, session__started_at__date=today)
            
            perf.total_requests = records.count()
            perf.pending_requests = records.filter(status='PENDING').count()
            perf.approved_requests = records.filter(status='APPROVED').count()
            perf.rejected_requests = records.filter(status='REJECTED').count()
            
            # Calculate rates
            if perf.total_requests > 0:
                perf.approval_rate = (perf.approved_requests / perf.total_requests) * 100
                perf.rejection_rate = (perf.rejected_requests / perf.total_requests) * 100
            
            # Calculate response times
            approved_records = records.filter(status='APPROVED', approved_at__isnull=False)
            total_hours = 0
            resp_count = 0
            
            for rec in approved_records:
                if rec.approved_at and rec.created_at:
                    delta = rec.approved_at - rec.created_at
                    hours = delta.total_seconds() / 3600
                    total_hours += hours
                    resp_count += 1
            
            perf.avg_response_hours = total_hours / resp_count if resp_count > 0 else 0
            perf.save()
        
        self.stdout.write(self.style.SUCCESS('Successfully updated report statistics'))
