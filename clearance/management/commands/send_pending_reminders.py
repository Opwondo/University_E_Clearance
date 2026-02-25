from django.core.management.base import BaseCommand
from clearance.utils.email_utils import EmailNotificationService

class Command(BaseCommand):
    help = 'Send pending clearance reminders to officers'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=1,
            help='Number of days to look back for pending clearances'
        )
    
    def handle(self, *args, **options):
        self.stdout.write('Sending pending clearance reminders...')
        
        notifications = EmailNotificationService.send_pending_reminder_to_officers()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully sent {len(notifications)} reminders')
        )
