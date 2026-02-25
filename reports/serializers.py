from rest_framework import serializers
from .models import ClearanceStatistics, DepartmentPerformance, StudentProgress

class ClearanceStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClearanceStatistics
        fields = '__all__'

class DepartmentPerformanceSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = DepartmentPerformance
        fields = '__all__'

class StudentProgressSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    admission_number = serializers.CharField(source='student.admission_number', read_only=True)
    
    class Meta:
        model = StudentProgress
        fields = '__all__'
