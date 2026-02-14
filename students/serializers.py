from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import StudentProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['id']

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='STUDENT'),
        source='user',
        write_only=True
    )
    clearance_status = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentProfile
        fields = [
            'id', 'user', 'user_id', 'admission_number', 'registration_number',
            'faculty', 'department', 'course', 'year_of_study',
            'date_of_birth', 'address', 'phone_number', 'status',
            'clearance_status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'clearance_status']
    
    def get_clearance_status(self, obj):
        return obj.get_clearance_status()
    
    def validate_admission_number(self, value):
        if StudentProfile.objects.exclude(pk=self.instance.pk if self.instance else None)\
                                  .filter(admission_number=value).exists():
            raise serializers.ValidationError("Admission number already exists")
        return value
    
    def validate_registration_number(self, value):
        if StudentProfile.objects.exclude(pk=self.instance.pk if self.instance else None)\
                                  .filter(registration_number=value).exists():
            raise serializers.ValidationError("Registration number already exists")
        return value
