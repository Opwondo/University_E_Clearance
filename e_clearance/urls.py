from django.contrib import admin
from django.urls import path, include

from reports import views_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')), 
    path('api/students/', include('students.urls')),
    path('api/departments/', include('departments.urls')),
    path('api/clearance/', include('clearance.urls')),
    path('api/audit/', include('audit.urls')),
    path('api/reports/', include('reports.urls')),
    path('dashboard/', views_dashboard.DashboardTemplateView.as_view(), name='dashboard-html'),
    path('api/certificates/', include('certificates.urls')),

]
