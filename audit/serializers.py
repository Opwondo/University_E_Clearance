from rest_framework import serializers
from .models import AuditLog

class AuditLogSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    action_type_display = serializers.CharField(source='get_action_type_display', read_only=True)
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'user_full_name', 'username', 'user_role',
            'action_type', 'action_type_display', 'action_description',
            'entity_type', 'entity_id', 'entity_repr',
            'before_state', 'after_state',
            'ip_address', 'user_agent', 'request_method', 'request_path',
            'status', 'timestamp', 'time_ago'
        ]
        read_only_fields = fields
    
    def get_time_ago(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        
        delta = timezone.now() - obj.timestamp
        
        if delta < timedelta(minutes=1):
            return 'just now'
        elif delta < timedelta(hours=1):
            minutes = int(delta.total_seconds() / 60)
            return f'{minutes} minute{"s" if minutes != 1 else ""} ago'
        elif delta < timedelta(days=1):
            hours = int(delta.total_seconds() / 3600)
            return f'{hours} hour{"s" if hours != 1 else ""} ago'
        elif delta < timedelta(days=7):
            days = delta.days
            return f'{days} day{"s" if days != 1 else ""} ago'
        else:
            return obj.timestamp.strftime('%Y-%m-%d %H:%M')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Pretty print JSON fields if they exist
        if data.get('before_state'):
            data['before_state'] = instance.before_state
        if data.get('after_state'):
            data['after_state'] = instance.after_state
            
        return data
