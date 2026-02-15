from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    ClearanceWorkflow, WorkflowStage, WorkflowStageDepartment,
    ClearanceSession, ClearanceRecord, ClearanceComment
)
from students.serializers import StudentProfileSerializer
from departments.serializers import DepartmentSerializer

User = get_user_model()

class WorkflowStageDepartmentSerializer(serializers.ModelSerializer):
    department_details = DepartmentSerializer(source='department', read_only=True)
    
    class Meta:
        model = WorkflowStageDepartment
        fields = ['id', 'department', 'department_details', 'order_within_stage', 'is_mandatory']

class WorkflowStageSerializer(serializers.ModelSerializer):
    departments = WorkflowStageDepartmentSerializer(source='workflowstagedepartment_set', many=True, read_only=True)
    
    class Meta:
        model = WorkflowStage
        fields = ['id', 'name', 'stage_order', 'description', 'departments']

class ClearanceWorkflowSerializer(serializers.ModelSerializer):
    stages = WorkflowStageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ClearanceWorkflow
        fields = ['id', 'name', 'session_type', 'description', 'is_active', 'stages', 'created_at']

class ClearanceRecordSerializer(serializers.ModelSerializer):
    department_details = DepartmentSerializer(source='department', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    can_approve = serializers.SerializerMethodField()
    
    class Meta:
        model = ClearanceRecord
        fields = [
            'id', 'department', 'department_details', 'status',
            'approved_by', 'approved_by_name', 'approved_at',
            'remarks', 'created_at', 'updated_at', 'can_approve'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'approved_at']
    
    def get_can_approve(self, obj):
        request = self.context.get('request')
        if request and request.user:
            # Check if user is officer of this department
            if request.user.role == 'OFFICER' and request.user in obj.department.officers.all():
                return obj.can_approve()
        return False

class ClearanceSessionSerializer(serializers.ModelSerializer):
    student_details = StudentProfileSerializer(source='student', read_only=True)
    workflow_details = ClearanceWorkflowSerializer(source='workflow', read_only=True)
    records = ClearanceRecordSerializer(many=True, read_only=True)
    progress_percentage = serializers.IntegerField(source='get_progress_percentage', read_only=True)
    current_stage_progress = serializers.IntegerField(source='get_current_stage_progress', read_only=True)
    
    class Meta:
        model = ClearanceSession
        fields = [
            'id', 'student', 'student_details', 'workflow', 'workflow_details',
            'status', 'current_stage', 'progress_percentage', 'current_stage_progress',
            'started_at', 'completed_at', 'last_activity', 'remarks', 'records'
        ]
        read_only_fields = ['id', 'started_at', 'last_activity', 'completed_at']

class ClearanceCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = ClearanceComment
        fields = ['id', 'record', 'author', 'author_name', 'comment', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']

class ApproveRejectSerializer(serializers.Serializer):
    remarks = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        # Add any validation logic here
        return data
