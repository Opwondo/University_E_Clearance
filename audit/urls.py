from django.urls import path
from . import views

urlpatterns = [
    path('logs/', views.AuditLogListView.as_view(), name='audit-log-list'),
    path('logs/<int:pk>/', views.AuditLogDetailView.as_view(), name='audit-log-detail'),
    path('logs/recent/', views.RecentActivitiesView.as_view(), name='recent-activities'),
    path('logs/user/<int:user_id>/', views.UserAuditLogsView.as_view(), name='user-audit-logs'),
    path('logs/entity/<str:entity_type>/<int:entity_id>/', views.EntityAuditLogsView.as_view(), name='entity-audit-logs'),
    path('logs/stats/summary/', views.AuditLogStatsView.as_view(), name='audit-log-stats'),
]
