from django.contrib import admin
from django.urls import path, include
from e_clearance import views as project_views  
from reports import views as reports_views      
from reports import views_dashboard

urlpatterns = [
    # Root endpoint - using the alias
    path('', project_views.api_root, name='api-root'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('accounts.urls')),
    path('api/students/', include('students.urls')),
    path('api/departments/', include('departments.urls')),
    path('api/clearance/', include('clearance.urls')),
    path('api/audit/', include('audit.urls')),
    path('api/reports/', include('reports.urls')),
    
    # Dashboard - using the correct import
    path('dashboard/', views_dashboard.DashboardTemplateView.as_view(), name='dashboard-html'),
    
    # Certificates
    path('api/certificates/', include('certificates.urls')),
]