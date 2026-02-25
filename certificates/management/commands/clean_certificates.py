from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from certificates.models import GeneratedCertificate
import os

class Command(BaseCommand):
    help = 'Clean up old/unused certificates'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Delete certificates older than N days (default: 30)'
        )
        
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting'
        )
    
    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']
        
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Find old certificates
        old_certificates = GeneratedCertificate.objects.filter(
            issue_date__lt=cutoff_date
        )
        
        count = old_certificates.count()
        
        if dry_run:
            self.stdout.write(f"Would delete {count} certificates older than {days} days")
            return
        
        # Delete files and database records
        for cert in old_certificates:
            if cert.pdf_file:
                if os.path.exists(cert.pdf_file.path):
                    os.remove(cert.pdf_file.path)
        
        deleted = old_certificates.delete()[0]
        
        self.stdout.write(
            self.style.SUCCESS(f"Successfully deleted {deleted} old certificates")
        )
