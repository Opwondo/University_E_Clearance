from rest_framework import serializers
from .models import EmailNotification

class EmailNotificationSerializer(serializers.ModelSerializer):
    recipient_name = serializers.CharField(source='recipient.get_full_name', read_only=True)
    recipient_email = serializers.EmailField(source='recipient.email', read_only=True)
    
    class Meta:
        model = EmailNotification
        fields = [
            'id', 'recipient', 'recipient_name', 'recipient_email',
            'notification_type', 'subject', 'body',
            'session', 'record', 'sent_at', 'is_sent', 'error_message',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'sent_at', 'is_sent', 'error_message']
