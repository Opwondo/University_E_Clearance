from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Avg, Q, F, Sum
from django.db.models.functions import TruncDate, TruncMonth, TruncYear
from django.utils import timezone
from datetime import timedelta, datetime
from collections import defaultdict
from clearance.models import ClearanceSession, ClearanceRecord
from students.models import StudentProfile
from departments.models import Department
from accounts.permissions import IsAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

class DashboardOverviewView(APIView):
    """
    GET: Get overview statistics for the dashboard
    """
    permission_classes = [IsAdmin]
    
    def get(self, request):
        # Date range filters
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        
        date_filter = request.query_params.get('period', '30d')
        if date_filter == '7d':
            start_date = end_date - timedelta(days=7)
        elif date_filter == '90d':
            start_date = end_date - timedelta(days=90)
        elif date_filter == '1y':
            start_date = end_date - timedelta(days=365)
        
        # Get all sessions within date range
        sessions = ClearanceSession.objects.filter(
            started_at__gte=start_date,
            started_at__lte=end_date
        )
        
        # Overview stats
        total_sessions = sessions.count()
        completed_sessions = sessions.filter(status='COMPLETED').count()
        in_progress = sessions.filter(status='IN_PROGRESS').count()
        blocked = sessions.filter(status='BLOCKED').count()
        draft = sessions.filter(status='DRAFT').count()
        
        # Calculate completion rate
        completion_rate = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
        
        # Get department stats
        departments = Department.objects.filter(is_active=True)
        total_departments = departments.count()
        
        # Get student stats
        total_students = StudentProfile.objects.count()
        students_with_clearance = StudentProfile.objects.filter(
            clearance_sessions__status='COMPLETED'
        ).distinct().count()
        
        # Calculate average completion time
        completed_sessions_data = sessions.filter(
            status='COMPLETED',
            completed_at__isnull=False
        )
        
        total_completion_time = 0
        completion_count = 0
        
        for session in completed_sessions_data:
            if session.completed_at and session.started_at:
                delta = session.completed_at - session.started_at
                days = delta.total_seconds() / 86400  # Convert to days
                total_completion_time += days
                completion_count += 1
        
        avg_completion_days = total_completion_time / completion_count if completion_count > 0 else 0
        
        response_data = {
            'date_range': {
                'start': start_date.date(),
                'end': end_date.date(),
                'period': date_filter
            },
            'overview': {
                'total_sessions': total_sessions,
                'completed_sessions': completed_sessions,
                'in_progress': in_progress,
                'blocked': blocked,
                'draft': draft,
                'completion_rate': round(completion_rate, 1)
            },
            'students': {
                'total': total_students,
                'cleared': students_with_clearance,
                'clearance_rate': round((students_with_clearance / total_students * 100), 1) if total_students > 0 else 0
            },
            'departments': {
                'total': total_departments
            },
            'performance': {
                'avg_completion_days': round(avg_completion_days, 1)
            }
        }
        
        return Response(response_data)

class ClearanceTrendsView(APIView):
    """
    GET: Get clearance trends over time
    """
    permission_classes = [IsAdmin]
    
    def get(self, request):
        # Get group by parameter (day, month, year)
        group_by = request.query_params.get('group_by', 'day')
        
        # Date range
        end_date = timezone.now()
        start_date = end_date - timedelta(days=90)  # Last 90 days
        
        sessions = ClearanceSession.objects.filter(
            started_at__gte=start_date,
            started_at__lte=end_date
        )
        
        # Group by date
        if group_by == 'day':
            sessions = sessions.annotate(date=TruncDate('started_at'))
        elif group_by == 'month':
            sessions = sessions.annotate(date=TruncMonth('started_at'))
        elif group_by == 'year':
            sessions = sessions.annotate(date=TruncYear('started_at'))
        
        # Aggregate data
        trends = sessions.values('date').annotate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='COMPLETED')),
            in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
            blocked=Count('id', filter=Q(status='BLOCKED'))
        ).order_by('date')
        
        # Format for chart
        labels = []
        total_data = []
        completed_data = []
        in_progress_data = []
        
        for item in trends:
            labels.append(item['date'].strftime('%Y-%m-%d'))
            total_data.append(item['total'])
            completed_data.append(item['completed'])
            in_progress_data.append(item['in_progress'])
        
        return Response({
            'labels': labels,
            'datasets': {
                'total': total_data,
                'completed': completed_data,
                'in_progress': in_progress_data
            }
        })

class DepartmentPerformanceView(APIView):
    """
    GET: Get department performance metrics
    """
    permission_classes = [IsAdmin]
    
    def get(self, request):
        departments = Department.objects.filter(is_active=True)
        
        performance_data = []
        
        for dept in departments:
            # Get clearance records for this department
            records = ClearanceRecord.objects.filter(department=dept)
            
            total = records.count()
            approved = records.filter(status='APPROVED').count()
            rejected = records.filter(status='REJECTED').count()
            pending = records.filter(status='PENDING').count()
            
            # Calculate average response time
            approved_records = records.filter(
                status='APPROVED',
                approved_at__isnull=False,
                created_at__isnull=False
            )
            
            total_response_time = 0
            response_count = 0
            
            for record in approved_records:
                if record.approved_at and record.created_at:
                    delta = record.approved_at - record.created_at
                    hours = delta.total_seconds() / 3600
                    total_response_time += hours
                    response_count += 1
            
            avg_response_hours = total_response_time / response_count if response_count > 0 else 0
            
            performance_data.append({
                'department_id': dept.id,
                'department_name': dept.name,
                'department_type': dept.department_type,
                'total_requests': total,
                'approved': approved,
                'rejected': rejected,
                'pending': pending,
                'approval_rate': round((approved / total * 100), 1) if total > 0 else 0,
                'rejection_rate': round((rejected / total * 100), 1) if total > 0 else 0,
                'avg_response_hours': round(avg_response_hours, 1)
            })
        
        # Sort by pending count (highest first)
        performance_data.sort(key=lambda x: x['pending'], reverse=True)
        
        return Response(performance_data)

class StudentProgressListView(APIView):
    """
    GET: Get student progress list with filters
    """
    permission_classes = [IsAdmin]
    
    def get(self, request):
        # Get filter parameters
        status_filter = request.query_params.get('status', '')
        search = request.query_params.get('search', '')
        
        students = StudentProfile.objects.all().select_related('user')
        
        # Apply search
        if search:
            students = students.filter(
                Q(user__username__icontains=search) |
                Q(user__email__icontains=search) |
                Q(admission_number__icontains=search)
            )
        
        progress_data = []
        
        for student in students:
            # Get the most recent session
            latest_session = student.clearance_sessions.order_by('-started_at').first()
            
            if latest_session:
                total_depts = latest_session.records.count()
                completed_depts = latest_session.records.filter(status='APPROVED').count()
                progress = (completed_depts / total_depts * 100) if total_depts > 0 else 0
                
                status = latest_session.status
            else:
                progress = 0
                status = 'NO_SESSION'
            
            # Apply status filter
            if status_filter and status_filter != status:
                continue
            
            progress_data.append({
                'student_id': student.id,
                'name': student.user.get_full_name() or student.user.username,
                'admission_number': student.admission_number,
                'email': student.user.email,
                'faculty': student.faculty,
                'department': student.department,
                'course': student.course,
                'progress': round(progress, 1),
                'status': status,
                'last_activity': latest_session.last_activity if latest_session else None
            })
        
        return Response(progress_data)

class ClearanceHeatmapView(APIView):
    """
    GET: Get clearance activity heatmap data
    """
    permission_classes = [IsAdmin]
    
    def get(self, request):
        # Get last 365 days
        end_date = timezone.now()
        start_date = end_date - timedelta(days=365)
        
        # Get daily counts
        daily_counts = ClearanceSession.objects.filter(
            started_at__gte=start_date,
            started_at__lte=end_date
        ).annotate(
            date=TruncDate('started_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        # Format for heatmap
        heatmap_data = []
        current_date = start_date.date()
        
        count_dict = {item['date']: item['count'] for item in daily_counts}
        
        while current_date <= end_date.date():
            heatmap_data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'count': count_dict.get(current_date, 0)
            })
            current_date += timedelta(days=1)
        
        return Response(heatmap_data)

class ExportReportView(APIView):
    """
    GET: Export report data in various formats
    """
    permission_classes = [IsAdmin]
    
    def get(self, request):
        report_type = request.query_params.get('type', 'summary')
        format_type = request.query_params.get('format', 'json')
        
        if report_type == 'summary':
            data = self.get_summary_report()
        elif report_type == 'departments':
            data = self.get_department_report()
        elif report_type == 'students':
            data = self.get_student_report()
        else:
            return Response({'error': 'Invalid report type'}, status=status.HTTP_400_BAD_REQUEST)
        
        if format_type == 'json':
            return Response(data)
        elif format_type == 'csv':
            # For CSV, you'd need to implement CSV rendering
            return Response({'message': 'CSV export coming soon'})
        else:
            return Response({'error': 'Invalid format'}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_summary_report(self):
        """Generate summary report"""
        total_sessions = ClearanceSession.objects.count()
        completed = ClearanceSession.objects.filter(status='COMPLETED').count()
        
        return {
            'generated_at': timezone.now(),
            'summary': {
                'total_sessions': total_sessions,
                'completed_sessions': completed,
                'completion_rate': round((completed / total_sessions * 100), 1) if total_sessions > 0 else 0
            }
        }
    
    def get_department_report(self):
        """Generate department performance report"""
        departments = Department.objects.all()
        report = []
        
        for dept in departments:
            records = ClearanceRecord.objects.filter(department=dept)
            report.append({
                'department': dept.name,
                'total_requests': records.count(),
                'approved': records.filter(status='APPROVED').count(),
                'rejected': records.filter(status='REJECTED').count(),
                'pending': records.filter(status='PENDING').count()
            })
        
        return report
    
    def get_student_report(self):
        """Generate student progress report"""
        students = StudentProfile.objects.all()
        report = []
        
        for student in students:
            sessions = student.clearance_sessions.count()
            completed = student.clearance_sessions.filter(status='COMPLETED').exists()
            
            report.append({
                'student': student.user.username,
                'admission': student.admission_number,
                'total_sessions': sessions,
                'has_completed': completed
            })
        
        return report
