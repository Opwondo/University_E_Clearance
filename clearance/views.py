from rest_framework import generics, permissions, filters, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404
from clearance.utils import EmailNotificationService
from .models import ClearanceSession, ClearanceRecord, ClearanceWorkflow, ClearanceComment
from .serializers import (
    ClearanceSessionSerializer, ClearanceRecordSerializer,
    ClearanceWorkflowSerializer, ClearanceCommentSerializer,
    ApproveRejectSerializer
)
from .permissions import IsStudentOwner, IsAssignedOfficer, CanApproveClearance
from accounts.permissions import IsAdmin, IsOfficer, IsStudent

class WorkflowListView(generics.ListAPIView):
    """
    GET: List all active clearance workflows
    """
    queryset = ClearanceWorkflow.objects.filter(is_active=True)
    serializer_class = ClearanceWorkflowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class ClearanceSessionListCreateView(generics.ListCreateAPIView):
    """
    GET: List clearance sessions (filtered by user role)
    POST: Create new clearance session (Students only)
    """
    serializer_class = ClearanceSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'workflow']
    search_fields = ['student__admission_number', 'student__user__username']
    ordering_fields = ['started_at', 'last_activity']
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'ADMIN':
            # Admins see all sessions
            return ClearanceSession.objects.all()
        
        elif user.role == 'OFFICER':
            # Officers see sessions for their departments
            return ClearanceSession.objects.filter(
                Q(records__department__officers=user) |
                Q(student__user=user)  # Also see if they're also a student
            ).distinct()
        
        elif user.role == 'STUDENT':
            # Students see only their own sessions
            return ClearanceSession.objects.filter(student__user=user)
        
        return ClearanceSession.objects.none()
    
    def perform_create(self, serializer):
        # Students can only create sessions for themselves
        if self.request.user.role == 'STUDENT':
            student_profile = self.request.user.student_profile
            workflow = get_object_or_404(ClearanceWorkflow, id=self.request.data.get('workflow'))
            
            # Check if student already has an active session
            active_session = ClearanceSession.objects.filter(
                student=student_profile,
                status__in=['DRAFT', 'IN_PROGRESS']
            ).exists()
            
            if active_session:
                raise serializers.ValidationError(
                    "You already have an active clearance session"
                )
            
            session = serializer.save(
                student=student_profile,
                created_by=self.request.user,
                status='DRAFT'
            )
            
            # Create clearance records for all departments in workflow
            self._create_clearance_records(session)
            
            # =====  EMAIL NOTIFICATION AFTER SESSION CREATION =====
            EmailNotificationService.send_session_created_notification(session, self.request)
            # ==========================================================
    
    def _create_clearance_records(self, session):
        """Create clearance records for all departments in the workflow"""
        from .models import WorkflowStageDepartment
        
        stage_depts = WorkflowStageDepartment.objects.filter(
            stage__workflow=session.workflow
        ).select_related('department')
        
        for stage_dept in stage_depts:
            ClearanceRecord.objects.create(
                session=session,
                department=stage_dept.department,
                status='PENDING'
            )

class ClearanceSessionDetailView(generics.RetrieveAPIView):
    """
    GET: Get detailed clearance session information
    """
    queryset = ClearanceSession.objects.all()
    serializer_class = ClearanceSessionSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudentOwner | IsAssignedOfficer | IsAdmin]

class PendingClearancesView(generics.ListAPIView):
    """
    GET: Get pending clearances for the current officer's departments
    """
    serializer_class = ClearanceRecordSerializer
    permission_classes = [IsOfficer]
    
    def get_queryset(self):
        return ClearanceRecord.objects.filter(
            department__officers=self.request.user,
            status='PENDING',
            session__status='IN_PROGRESS'
        ).select_related('session', 'department', 'session__student')

class ClearanceRecordDetailView(generics.RetrieveAPIView):
    """
    GET: Get clearance record details
    """
    queryset = ClearanceRecord.objects.all()
    serializer_class = ClearanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

class ApproveClearanceView(APIView):
    """
    POST: Approve a clearance record
    """
    permission_classes = [IsOfficer, CanApproveClearance]
    
    def post(self, request, pk):
        record = get_object_or_404(ClearanceRecord, pk=pk)
        
        # Check permissions
        self.check_object_permissions(request, record)
        
        serializer = ApproveRejectSerializer(data=request.data)
        if serializer.is_valid():
            # Update record
            record.status = 'APPROVED'
            record.approved_by = request.user
            record.approved_at = timezone.now()
            record.remarks = serializer.validated_data.get('remarks', '')
            record.save()
            
            # Send approval notification
            EmailNotificationService.send_record_approved_notification(record, self.request)

            # Update session status
            session = record.session
            self._update_session_progress(session)
            
            # Create comment if remarks provided
            if serializer.validated_data.get('remarks'):
                ClearanceComment.objects.create(
                    record=record,
                    author=request.user,
                    comment=serializer.validated_data['remarks']
                )
            
            return Response({
                'status': 'approved',
                'record': ClearanceRecordSerializer(record, context={'request': request}).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _update_session_progress(self, session):
        """Update session status based on progress"""
        total_records = session.records.count()
        approved_records = session.records.filter(status='APPROVED').count()
        
        if approved_records == total_records:
            session.status = 'COMPLETED'
            session.completed_at = timezone.now()
            # Send completion notification
            EmailNotificationService.send_session_completed_notification(session, self.request)
        elif session.status == 'DRAFT':
            session.status = 'IN_PROGRESS'
        
        # Update current stage
        self._update_current_stage(session)
        
        session.save()
    
    def _update_current_stage(self, session):
        """Determine and set the current stage"""
        from .models import WorkflowStage
        
        stages = WorkflowStage.objects.filter(
            workflow=session.workflow
        ).order_by('stage_order')
        
        for stage in stages:
            stage_depts = stage.workflowstagedepartment_set.all()
            all_approved = True
            
            for stage_dept in stage_depts:
                try:
                    record = session.records.get(department=stage_dept.department)
                    if record.status != 'APPROVED':
                        all_approved = False
                        break
                except ClearanceRecord.DoesNotExist:
                    all_approved = False
                    break
            
            if not all_approved:
                session.current_stage = stage
                break

class RejectClearanceView(APIView):
    """
    POST: Reject a clearance record
    """
    permission_classes = [IsOfficer, CanApproveClearance]
    
    def post(self, request, pk):
        record = get_object_or_404(ClearanceRecord, pk=pk)
        
        # Check permissions
        self.check_object_permissions(request, record)
        
        serializer = ApproveRejectSerializer(data=request.data)
        if serializer.is_valid():
            if not serializer.validated_data.get('remarks'):
                return Response(
                    {'remarks': ['Remarks are required for rejection']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Update record
            record.status = 'REJECTED'
            record.approved_by = request.user
            record.approved_at = timezone.now()
            record.remarks = serializer.validated_data['remarks']
            record.save()
            
            # Send rejection notification
            EmailNotificationService.send_record_rejected_notification(record, self.request)
            
            # Update session status
            session = record.session
            session.status = 'BLOCKED'
            session.save()
            
            # Create comment
            ClearanceComment.objects.create(
                record=record,
                author=request.user,
                comment=serializer.validated_data['remarks']
            )
            
            return Response({
                'status': 'rejected',
                'record': ClearanceRecordSerializer(record, context={'request': request}).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClearanceCommentsView(generics.ListCreateAPIView):
    """
    GET: Get comments for a clearance record
    POST: Add comment to clearance record
    """
    serializer_class = ClearanceCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        record_id = self.kwargs['record_id']
        return ClearanceComment.objects.filter(record_id=record_id)
    
    def perform_create(self, serializer):
        record = get_object_or_404(ClearanceRecord, pk=self.kwargs['record_id'])
        serializer.save(
            record=record,
            author=self.request.user
        )

class StudentClearanceSummaryView(APIView):
    """
    GET: Get clearance summary for the current student
    """
    permission_classes = [IsStudent]
    
    def get(self, request):
        student_profile = request.user.student_profile
        
        # Get active session
        active_session = ClearanceSession.objects.filter(
            student=student_profile,
            status__in=['DRAFT', 'IN_PROGRESS']
        ).first()
        
        # Get completed sessions
        completed_sessions = ClearanceSession.objects.filter(
            student=student_profile,
            status='COMPLETED'
        ).count()
        
        # Get pending departments
        if active_session:
            pending_records = active_session.records.filter(status='PENDING')
            pending_departments = [
                {
                    'id': r.department.id,
                    'name': r.department.name,
                    'type': r.department.department_type
                }
                for r in pending_records
            ]
        else:
            pending_departments = []
        
        return Response({
            'has_active_session': active_session is not None,
            'active_session_id': active_session.id if active_session else None,
            'progress': active_session.get_progress_percentage() if active_session else 0,
            'completed_sessions': completed_sessions,
            'pending_departments': pending_departments
        })