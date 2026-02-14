from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Department

User = get_user_model()

class UserBasicSerializer(serializers.ModelSerializer):
    """Basic User serializer for nested representation"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']

class DepartmentSerializer(serializers.ModelSerializer):
    """Department serializer with nested relationships"""
    officers = UserBasicSerializer(many=True, read_only=True)
    officer_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.filter(role='OFFICER'),
        source='officers',
        write_only=True,
        required=False
    )
    parent_department_name = serializers.CharField(
        source='parent_department.name',
        read_only=True
    )
    pending_clearances_count = serializers.SerializerMethodField()
    sub_departments_count = serializers.IntegerField(
        source='sub_departments.count',
        read_only=True
    )
    
    class Meta:
        model = Department
        fields = [
            'id', 'name', 'code', 'department_type', 'description',
            'officers', 'officer_ids', 'parent_department', 'parent_department_name',
            'is_active', 'pending_clearances_count', 'sub_departments_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_pending_clearances_count(self, obj):
        return obj.get_pending_clearances()
    
    def validate_code(self, value):
        """Ensure department code is unique"""
        if Department.objects.exclude(pk=self.instance.pk if self.instance else None)\
                              .filter(code=value).exists():
            raise serializers.ValidationError("Department code already exists")
        return value.upper()
    
    def validate(self, data):
        """Validate department hierarchy"""
        if 'parent_department' in data and data['parent_department']:
            # Prevent circular references
            if self.instance and data['parent_department'] == self.instance:
                raise serializers.ValidationError(
                    "Department cannot be its own parent"
                )
            
            # Check for circular hierarchy
            parent = data['parent_department']
            while parent:
                if parent == self.instance:
                    raise serializers.ValidationError(
                        "Circular department hierarchy detected"
                    )
                parent = parent.parent_department
        
        return data

class DepartmentListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    pending_clearances_count = serializers.SerializerMethodField()
    officers_count = serializers.IntegerField(source='officers.count', read_only=True)
    
    class Meta:
        model = Department
        fields = [
            'id', 'name', 'code', 'department_type', 
            'is_active', 'pending_clearances_count', 'officers_count'
        ]
    
    def get_pending_clearances_count(self, obj):
        return obj.get_pending_clearances()
