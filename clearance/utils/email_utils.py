from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from celery import shared_task
from ..models import EmailNotification

class EmailNotificationService:
    """
    Service class for sending email notifications
    """
    
    @staticmethod
    def get_portal_url(request=None):
        """Get base portal URL"""
        if request:
            return request.build_absolute_uri('/')
        return 'http://localhost:8000'
    
    @staticmethod
    @shared_task
    def send_email_task(notification_id):
        """
        Celery task to send email
        """
        try:
            notification = EmailNotification.objects.get(id=notification_id)
            
            # Send email
            send_mail(
                subject=notification.subject,
                message=notification.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[notification.recipient.email],
                fail_silently=False,
                html_message=notification.body
            )
            
            # Update notification status
            notification.is_sent = True
            notification.sent_at = timezone.now()
            notification.save()
            
            return f"Email sent to {notification.recipient.email}"
            
        except Exception as e:
            try:
                notification = EmailNotification.objects.get(id=notification_id)
                notification.error_message = str(e)
                notification.save()
            except:
                pass
            return f"Error sending email: {str(e)}"
    
    @classmethod
    def send_session_created_notification(cls, session, request=None):
        """Send notification when clearance session is created"""
        student = session.student
        user = student.user
        
        context = {
            'student_name': user.get_full_name() or user.username,
            'session_id': session.id,
            'workflow_name': session.workflow.name,
            'started_at': session.started_at,
            'total_departments': session.records.count(),
            'portal_url': f"{cls.get_portal_url(request)}/dashboard"
        }
        
        html_message = render_to_string('emails/session_created.html', context)
        subject = f"Clearance Session Created - {session.workflow.name}"
        
        notification = EmailNotification.objects.create(
            recipient=user,
            notification_type='SESSION_CREATED',
            subject=subject,
            body=html_message,
            session=session
        )
        
        cls.send_email_task.delay(notification.id)
        return notification
    
    @classmethod
    def send_record_approved_notification(cls, record, request=None):
        """Send notification when a department approves clearance"""
        student = record.session.student
        user = student.user
        
        total_records = record.session.records.count()
        completed_records = record.session.records.filter(status='APPROVED').count()
        
        context = {
            'student_name': user.get_full_name() or user.username,
            'department_name': record.department.name,
            'officer_name': record.approved_by.get_full_name() if record.approved_by else 'Officer',
            'approved_at': record.approved_at,
            'remarks': record.remarks,
            'completed_departments': completed_records,
            'total_departments': total_records,
            'portal_url': f"{cls.get_portal_url(request)}/clearance/{record.session.id}"
        }
        
        html_message = render_to_string('emails/record_approved.html', context)
        subject = f"✅ {record.department.name} - Clearance Approved"
        
        notification = EmailNotification.objects.create(
            recipient=user,
            notification_type='RECORD_APPROVED',
            subject=subject,
            body=html_message,
            session=record.session,
            record=record
        )
        
        cls.send_email_task.delay(notification.id)
        return notification
    
    @classmethod
    def send_record_rejected_notification(cls, record, request=None):
        """Send notification when a department rejects clearance"""
        student = record.session.student
        user = student.user
        
        context = {
            'student_name': user.get_full_name() or user.username,
            'department_name': record.department.name,
            'officer_name': record.approved_by.get_full_name() if record.approved_by else 'Officer',
            'rejected_at': record.approved_at,
            'remarks': record.remarks,
            'portal_url': f"{cls.get_portal_url(request)}/clearance/{record.session.id}"
        }
        
        html_message = render_to_string('emails/record_rejected.html', context)
        subject = f"❌ {record.department.name} - Clearance Update"
        
        notification = EmailNotification.objects.create(
            recipient=user,
            notification_type='RECORD_REJECTED',
            subject=subject,
            body=html_message,
            session=record.session,
            record=record
        )
        
        cls.send_email_task.delay(notification.id)
        return notification
    
    @classmethod
    def send_session_completed_notification(cls, session, request=None):
        """Send notification when clearance is fully completed"""
        student = session.student
        user = student.user
        
        context = {
            'student_name': user.get_full_name() or user.username,
            'session_id': session.id,
            'completed_at': session.completed_at,
            'total_departments': session.records.count(),
            'portal_url': f"{cls.get_portal_url(request)}/certificate/{session.id}",
            'certificate_url': f"{cls.get_portal_url(request)}/api/clearance/certificate/{session.id}/download"
        }
        
        html_message = render_to_string('emails/session_completed.html', context)
        subject = "🎉 Clearance Successfully Completed!"
        
        notification = EmailNotification.objects.create(
            recipient=user,
            notification_type='SESSION_COMPLETED',
            subject=subject,
            body=html_message,
            session=session
        )
        
        cls.send_email_task.delay(notification.id)
        return notification
