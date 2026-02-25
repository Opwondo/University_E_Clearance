from django.db import models
from django.contrib.auth import get_user_model
from students.models import StudentProfile
from clearance.models import ClearanceSession

User = get_user_model()

class CertificateTemplate(models.Model):
    """
    Store certificate templates for different clearance types
    """
    name = models.CharField(max_length=100)
    template_type = models.CharField(
        max_length=50,
        choices=[
            ('GRADUATION', 'Graduation Clearance'),
            ('TRANSFER', 'Transfer Clearance'),
            ('INTERNSHIP', 'Internship Clearance'),
        ],
        unique=True
    )
    template_file = models.FileField(
        upload_to='certificates/templates/',
        help_text="HTML template file for certificate"
    )
    background_image = models.ImageField(
        upload_to='certificates/backgrounds/',
        null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'certificate_templates'
    
    def __str__(self):
        return f"{self.name} - {self.get_template_type_display()}"

class GeneratedCertificate(models.Model):
    """
    Store generated certificates for students
    """
    session = models.OneToOneField(
        ClearanceSession,
        on_delete=models.CASCADE,
        related_name='certificate'
    )
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='certificates'
    )
    
    # Certificate details
    certificate_number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    
    # File
    pdf_file = models.FileField(
        upload_to='certificates/generated/',
        help_text="Generated PDF certificate"
    )
    
    # Verification
    verification_code = models.CharField(max_length=100, unique=True)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='verified_certificates'
    )
    
    # Metadata
    download_count = models.IntegerField(default=0)
    last_downloaded = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'generated_certificates'
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"Certificate {self.certificate_number} - {self.student.user.get_full_name()}"
    
    def increment_download_count(self):
        """Increment download counter"""
        self.download_count += 1
        self.last_downloaded = timezone.now()
        self.save()
    
    @staticmethod
    def generate_certificate_number():
        """Generate unique certificate number"""
        import random
        import string
        from django.utils import timezone
        
        year = timezone.now().year
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return f"CERT-{year}-{random_part}"
    
    @staticmethod
    def generate_verification_code():
        """Generate unique verification code"""
        import uuid
        return str(uuid.uuid4()).replace('-', '')[:16].upper()
