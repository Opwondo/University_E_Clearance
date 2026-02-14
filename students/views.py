from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import StudentProfile
from .serializers import StudentProfileSerializer
from accounts.permissions import IsAdmin, IsOfficer, IsStudentOrReadOnly

class StudentProfileListCreateView(generics.ListCreateAPIView):
    """
    GET: List all student profiles (Admin/Officer only)
    POST: Create new student profile (Admin only)
    """
    queryset = StudentProfile.objects.all().order_by('-created_at')
    serializer_class = StudentProfileSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['faculty', 'department', 'course', 'year_of_study', 'status']
    search_fields = ['admission_number', 'registration_number', 'user__username', 'user__email']
    ordering_fields = ['created_at', 'admission_number', 'year_of_study']
    
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAdmin]
        else:
            self.permission_classes = [IsAdmin | IsOfficer]
        return super().get_permissions()

class StudentProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Get student profile details
    PUT/PATCH: Update student profile (Admin only)
    DELETE: Delete student profile (Admin only)
    """
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAdmin | IsOfficer | IsStudentOrReadOnly]
        else:
            self.permission_classes = [IsAdmin]
        return super().get_permissions()
    
    def get_object(self):
        obj = super().get_object()
        # Students can only view their own profile
        if self.request.user.role == 'STUDENT':
            if not hasattr(self.request.user, 'student_profile') or \
               obj.id != self.request.user.student_profile.id:
                self.permission_denied(self.request)
        return obj

class CurrentStudentProfileView(APIView):
    """
    GET: Get current student's profile
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if request.user.role != 'STUDENT':
            return Response(
                {"detail": "User is not a student"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            profile = request.user.student_profile
            serializer = StudentProfileSerializer(profile)
            return Response(serializer.data)
        except StudentProfile.DoesNotExist:
            return Response(
                {"detail": "Student profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )
