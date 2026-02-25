from rest_framework import serializers
from .models import CertificateTemplate, GeneratedCertificate

class CertificateTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateTemplate
        fields = '__all__'

class GeneratedCertificateSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_admission = serializers.CharField(source='student.admission_number', read_only=True)
    session_id = serializers.IntegerField(source='session.id', read_only=True)
    
    class Meta:
        model = GeneratedCertificate
        fields = [
            'id', 'certificate_number', 'verification_code',
            'student', 'student_name', 'student_admission',
            'session', 'session_id', 'issue_date',
            'pdf_file', 'download_count', 'last_downloaded',
            'is_verified', 'verified_at'
        ]
        read_only_fields = ['id', 'certificate_number', 'verification_code', 'issue_date']
