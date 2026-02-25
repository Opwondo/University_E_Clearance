from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import EmailNotification
from .serializers_email import EmailNotificationSerializer
from accounts.permissions import IsAdmin, IsOfficer

class EmailNotificationListView(generics.ListAPIView):
    """
    GET: List email notifications for the current user
    """
    serializer_class = EmailNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'ADMIN':
            return EmailNotification.objects.all()
        else:
            return EmailNotification.objects.filter(recipient=user)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class EmailNotificationDetailView(generics.RetrieveAPIView):
    """
    GET: Get details of a specific email notification
    """
    queryset = EmailNotification.objects.all()
    serializer_class = EmailNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return EmailNotification.objects.all()
        return EmailNotification.objects.filter(recipient=user)

class EmailNotificationStatsView(APIView):
    """
    GET: Get email notification statistics
    """
    permission_classes = [IsAdmin | IsOfficer]
    
    def get(self, request):
        # Total emails sent
        total_sent = EmailNotification.objects.filter(is_sent=True).count()
        total_failed = EmailNotification.objects.filter(is_sent=False).exclude(error_message='').count()
        total_pending = EmailNotification.objects.filter(is_sent=False, error_message='').count()
        
        # Emails by type
        by_type = {}
        for notification_type, _ in EmailNotification.NotificationType.choices:
            count = EmailNotification.objects.filter(
                notification_type=notification_type,
                is_sent=True
            ).count()
            by_type[notification_type] = count
        
        return Response({
            'total_sent': total_sent,
            'total_failed': total_failed,
            'total_pending': total_pending,
            'by_type': by_type,
            'success_rate': f"{(total_sent/(total_sent+total_failed)*100):.1f}%" if total_sent+total_failed > 0 else "0%"
        })
