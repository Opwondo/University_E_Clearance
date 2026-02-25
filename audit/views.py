from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import AuditLog
from .serializers import AuditLogSerializer
from accounts.permissions import IsAdmin

class AuditLogListView(generics.ListAPIView):
    """
    GET: List audit logs with filters (Admin only)
    """
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['action_type', 'user_role', 'status', 'entity_type']
    search_fields = ['username', 'action_description', 'entity_repr', 'ip_address']
    ordering_fields = ['timestamp', 'username']
    ordering = ['-timestamp']
    
    def get_queryset(self):
        queryset = AuditLog.objects.all()
        
        # Date range filters
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)
        
        # User filter
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        return queryset

class AuditLogDetailView(generics.RetrieveAPIView):
    """
    GET: Get detailed audit log entry (Admin only)
    """
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdmin]

class RecentActivitiesView(generics.ListAPIView):
    """
    GET: Get recent activities across the system
    """
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdmin]
    
    def get_queryset(self):
        limit = int(self.request.query_params.get('limit', 50))
        return AuditLog.objects.all()[:limit]

class UserAuditLogsView(generics.ListAPIView):
    """
    GET: Get audit logs for a specific user
    """
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdmin]
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return AuditLog.objects.filter(user_id=user_id)

class EntityAuditLogsView(generics.ListAPIView):
    """
    GET: Get audit logs for a specific entity
    """
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdmin]
    
    def get_queryset(self):
        entity_type = self.kwargs['entity_type']
        entity_id = self.kwargs['entity_id']
        return AuditLog.objects.filter(
            entity_type=entity_type,
            entity_id=entity_id
        )

class AuditLogStatsView(APIView):
    """
    GET: Get audit log statistics (Admin only)
    """
    permission_classes = [IsAdmin]
    
    def get(self, request):
        # Time periods
        now = timezone.now()
        today = now.date()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        stats = {
            'total_logs': AuditLog.objects.count(),
            'today': AuditLog.objects.filter(timestamp__date=today).count(),
            'this_week': AuditLog.objects.filter(timestamp__gte=week_ago).count(),
            'this_month': AuditLog.objects.filter(timestamp__gte=month_ago).count(),
            
            'by_action': dict(
                AuditLog.objects.values_list('action_type')
                .annotate(count=Count('id'))
                .order_by('-count')[:10]
            ),
            
            'by_user': list(
                AuditLog.objects.values('username', 'user_role')
                .annotate(count=Count('id'))
                .order_by('-count')[:10]
            ),
            
            'by_status': dict(
                AuditLog.objects.values_list('status')
                .annotate(count=Count('id'))
            ),
            
            'recent_errors': AuditLog.objects.filter(
                status__in=['FAILURE', 'ERROR']
            )[:10].values('timestamp', 'username', 'action_description')
        }
        
        return Response(stats)
