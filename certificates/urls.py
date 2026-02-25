from django.urls import path
from . import views

urlpatterns = [
    # Generate certificate for completed session
    path('generate/<int:session_id>/', views.GenerateCertificateView.as_view(), name='generate-certificate'),
    
    # Download certificate
    path('download/<int:certificate_id>/', views.DownloadCertificateView.as_view(), name='download-certificate'),
    
    # Certificate details
    path('<int:pk>/', views.CertificateDetailView.as_view(), name='certificate-detail'),
    
    # Student's certificates
    path('my-certificates/', views.StudentCertificatesView.as_view(), name='my-certificates'),
    
    # Public verification
    path('verify/', views.VerifyCertificateView.as_view(), name='verify-certificate'),
    
    # Template preview (admin only)
    path('template/preview/', views.CertificateTemplateView.as_view(), name='certificate-preview'),
]
