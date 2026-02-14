from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Department
from .serializers import DepartmentSerializer, DepartmentListSerializer
from accounts.permissions import IsAdmin, IsOfficer

class DepartmentListCreateView(generics.ListCreateAPIView):
    """
    GET: List all departments (Authenticated users)
    POST: Create new department (Admin only)
    """
    queryset = Department.objects.all().order_by('name')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department_type', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DepartmentListSerializer
        return DepartmentSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAdmin]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by parent department
        parent_id = self.request.query_params.get('parent')
        if parent_id:
            queryset = queryset.filter(parent_department_id=parent_id)
        
        # Filter departments with no parent (top-level)
        if self.request.query_params.get('top_level') == 'true':
            queryset = queryset.filter(parent_department__isnull=True)
        
        return queryset

class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Get department details
    PUT/PATCH: Update department (Admin/Officer)
    DELETE: Delete department (Admin only)
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.request.method == 'DELETE':
            self.permission_classes = [IsAdmin]
        else:
            # PUT/PATCH - Admin or Officer of this department
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()
    
    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        
        # For update operations, check if user is officer of this department
        if request.method in ['PUT', 'PATCH']:
            if not (request.user.role == 'ADMIN' or 
                   (request.user.role == 'OFFICER' and request.user in obj.officers.all())):
                self.permission_denied(
                    request,
                    message="You don't have permission to update this department"
                )
    
    def perform_destroy(self, instance):
        # Check if department has sub-departments
        if instance.sub_departments.exists():
            raise serializers.ValidationError(
                "Cannot delete department with sub-departments. Reassign or delete them first."
            )
        instance.delete()

class DepartmentOfficersView(APIView):
    """
    Manage department officers
    """
    permission_classes = [IsAdmin | IsOfficer]
    
    def get(self, request, pk):
        """Get officers for a department"""
        try:
            department = Department.objects.get(pk=pk)
            
            # Check if officer belongs to this department
            if request.user.role == 'OFFICER' and request.user not in department.officers.all():
                return Response(
                    {"detail": "You don't have permission to view officers of this department"},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            officers = department.officers.all()
            data = [{
                'id': officer.id,
                'username': officer.username,
                'email': officer.email,
                'first_name': officer.first_name,
                'last_name': officer.last_name
            } for officer in officers]
            
            return Response(data)
        except Department.DoesNotExist:
            return Response(
                {"detail": "Department not found"},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def post(self, request, pk):
        """Add officers to department"""
        try:
            department = Department.objects.get(pk=pk)
            officer_ids = request.data.get('officer_ids', [])
            
            if not officer_ids:
                return Response(
                    {"detail": "officer_ids required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            officers = User.objects.filter(id__in=officer_ids, role='OFFICER')
            department.officers.add(*officers)
            
            return Response(
                {"detail": f"Added {len(officers)} officers to department"},
                status=status.HTTP_200_OK
            )
        except Department.DoesNotExist:
            return Response(
                {"detail": "Department not found"},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def delete(self, request, pk):
        """Remove officers from department"""
        try:
            department = Department.objects.get(pk=pk)
            officer_ids = request.data.get('officer_ids', [])
            
            if not officer_ids:
                return Response(
                    {"detail": "officer_ids required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            officers = User.objects.filter(id__in=officer_ids)
            department.officers.remove(*officers)
            
            return Response(
                {"detail": f"Removed {len(officers)} officers from department"},
                status=status.HTTP_200_OK
            )
        except Department.DoesNotExist:
            return Response(
                {"detail": "Department not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class DepartmentHierarchyView(APIView):
    """
    Get department hierarchy tree
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        def build_tree(departments):
            tree = []
            for dept in departments:
                node = {
                    'id': dept.id,
                    'name': dept.name,
                    'code': dept.code,
                    'type': dept.department_type,
                    'children': build_tree(dept.sub_departments.all())
                }
                tree.append(node)
            return tree
        
        top_level = Department.objects.filter(parent_department__isnull=True)
        tree = build_tree(top_level)
        return Response(tree)
