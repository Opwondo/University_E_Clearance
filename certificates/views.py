import os
from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from clearance.models import ClearanceSession
from students.models import StudentProfile
from accounts.permissions import IsAdmin, IsStudent
from .models import CertificateTemplate, GeneratedCertificate
from .serializers import GeneratedCertificateSerializer

class GenerateCertificateView(APIView):
    """
    POST: Generate certificate for completed clearance session
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, session_id):
        try:
            session = ClearanceSession.objects.get(id=session_id)
        except ClearanceSession.DoesNotExist:
            return Response(
                {'error': 'Session not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check permissions
        if request.user.role == 'STUDENT':
            if session.student.user != request.user:
                return Response(
                    {'error': 'You can only generate certificates for your own sessions'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        # Check if session is completed
        if session.status != 'COMPLETED':
            return Response(
                {'error': 'Certificate can only be generated for completed sessions'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if certificate already exists
        if hasattr(session, 'certificate'):
            return Response({
                'message': 'Certificate already exists',
                'certificate': GeneratedCertificateSerializer(session.certificate).data
            }, status=status.HTTP_200_OK)
        
        # Generate certificate
        certificate = self._create_certificate(session)
        
        serializer = GeneratedCertificateSerializer(certificate)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def _create_certificate(self, session):
        """Create and generate PDF certificate"""
        student = session.student
        
        # Get template based on session type
        template_type = session.workflow.session_type
        try:
            template = CertificateTemplate.objects.get(
                template_type=template_type,
                is_active=True
            )
        except CertificateTemplate.DoesNotExist:
            # Use default template
            template = None
        
        # Prepare context for template
        context = {
            'student_name': student.user.get_full_name() or student.user.username,
            'admission_number': student.admission_number,
            'registration_number': student.registration_number,
            'faculty': student.faculty,
            'department': student.department,
            'course': student.course,
            'clearance_type': session.workflow.name,
            'certificate_number': GeneratedCertificate.generate_certificate_number(),
            'verification_code': GeneratedCertificate.generate_verification_code(),
            'issue_date': timezone.now(),
            'completed_date': session.completed_at,
        }
        
        # Render HTML
        html_string = render_to_string(
            'certificates/graduation_certificate.html',
            context
        )
        
        # Generate PDF
        font_config = FontConfiguration()
        pdf_file = HTML(string=html_string).write_pdf(
            stylesheets=[CSS(string='@page { size: A4 landscape; }')],
            font_config=font_config
        )
        
        # Save PDF file
        import os
        from django.core.files.base import ContentFile
        from django.conf import settings
        
        filename = f"certificate_{context['certificate_number']}.pdf"
        
        # Create certificate instance
        certificate = GeneratedCertificate(
            session=session,
            student=student,
            certificate_number=context['certificate_number'],
            verification_code=context['verification_code']
        )
        
        # Save PDF to FileField
        certificate.pdf_file.save(filename, ContentFile(pdf_file))
        certificate.save()
        
        return certificate

class DownloadCertificateView(APIView):
    """
    GET: Download certificate PDF
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, certificate_id):
        certificate = get_object_or_404(GeneratedCertificate, id=certificate_id)
        
        # Check permissions
        if request.user.role == 'STUDENT':
            if certificate.student.user != request.user:
                return Response(
                    {'error': 'You can only download your own certificates'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        # Increment download count
        certificate.increment_download_count()
        
        # Return PDF file
        response = FileResponse(
            certificate.pdf_file,
            content_type='application/pdf'
        )
        response['Content-Disposition'] = f'attachment; filename="{certificate.certificate_number}.pdf"'
        
        return response

class VerifyCertificateView(APIView):
    """
    POST: Verify certificate using verification code
    """
    permission_classes = [permissions.AllowAny]  # Public endpoint
    
    def post(self, request):
        verification_code = request.data.get('verification_code')
        
        try:
            certificate = GeneratedCertificate.objects.get(
                verification_code=verification_code
            )
            
            # Update verification status
            if not certificate.is_verified:
                certificate.is_verified = True
                certificate.verified_at = timezone.now()
                certificate.verified_by = request.user if request.user.is_authenticated else None
                certificate.save()
            
            return Response({
                'is_valid': True,
                'certificate_number': certificate.certificate_number,
                'student_name': certificate.student.user.get_full_name(),
                'admission_number': certificate.student.admission_number,
                'issue_date': certificate.issue_date,
                'verified_at': certificate.verified_at,
                'download_count': certificate.download_count
            })
            
        except GeneratedCertificate.DoesNotExist:
            return Response({
                'is_valid': False,
                'message': 'Invalid verification code'
            }, status=status.HTTP_404_NOT_FOUND)

class CertificateDetailView(generics.RetrieveAPIView):
    """
    GET: Get certificate details
    """
    queryset = GeneratedCertificate.objects.all()
    serializer_class = GeneratedCertificateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'ADMIN':
            return GeneratedCertificate.objects.all()
        elif user.role == 'STUDENT':
            return GeneratedCertificate.objects.filter(student__user=user)
        else:
            return GeneratedCertificate.objects.none()

class StudentCertificatesView(generics.ListAPIView):
    """
    GET: List certificates for current student
    """
    serializer_class = GeneratedCertificateSerializer
    permission_classes = [IsStudent]
    
    def get_queryset(self):
        return GeneratedCertificate.objects.filter(
            student__user=self.request.user
        ).order_by('-issue_date')

class CertificateTemplateView(APIView):
    """
    Preview certificate template (Admin only)
    """
    permission_classes = [IsAdmin]
    
    def get(self, request):
        student = StudentProfile.objects.first()
        if not student:
            return Response(
                {'error': 'No student found for preview'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        context = {
            'student_name': 'John Doe',
            'admission_number': 'ADM2024001',
            'registration_number': 'REG2024001',
            'faculty': 'Engineering',
            'department': 'Computer Science',
            'course': 'Software Engineering',
            'clearance_type': 'Graduation',
            'certificate_number': 'CERT-2024-ABCD1234',
            'verification_code': 'VERIFY-1234-5678',
            'issue_date': timezone.now(),
        }
        
        html_string = render_to_string(
            'certificates/graduation_certificate.html',
            context
        )
        
        return HttpResponse(html_string)
