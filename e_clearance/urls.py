from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')), 
    path('api/students/', include('students.urls')),
    path('api/departments/', include('departments.urls')),
    path('api/clearance/', include('clearance.urls')),
]
