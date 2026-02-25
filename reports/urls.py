from django.urls import path

from reports import views_dashboard
from . import views

urlpatterns = [
    # Dashboard overview
    path('dashboard/overview/', views.DashboardOverviewView.as_view(), name='dashboard-overview'),
    
    # Trends and analytics
    path('trends/clearance/', views.ClearanceTrendsView.as_view(), name='clearance-trends'),
    path('trends/heatmap/', views.ClearanceHeatmapView.as_view(), name='clearance-heatmap'),
    
    # Department performance
    path('departments/performance/', views.DepartmentPerformanceView.as_view(), name='department-performance'),
    
    # Student progress
    path('students/progress/', views.StudentProgressListView.as_view(), name='student-progress'),
    
    # Export
    path('export/', views.ExportReportView.as_view(), name='export-report'),
    
    path('dashboard/', views_dashboard.DashboardTemplateView.as_view(), name='dashboard-html'),

]
