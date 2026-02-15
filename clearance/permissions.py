from rest_framework import permissions

class IsStudentOwner(permissions.BasePermission):
    """
    Allow students to access only their own clearance sessions
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'STUDENT':
            return obj.student.user == request.user
        return True

class IsAssignedOfficer(permissions.BasePermission):
    """
    Allow officers to approve/reject clearances for their departments
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'OFFICER':
            # For ClearanceRecord objects
            if hasattr(obj, 'department'):
                return request.user in obj.department.officers.all()
            # For ClearanceSession objects (checking records)
            elif hasattr(obj, 'records'):
                # Check if officer is assigned to any pending department in this session
                pending_records = obj.records.filter(
                    department__officers=request.user,
                    status='PENDING'
                )
                return pending_records.exists()
        return False

class CanApproveClearance(permissions.BasePermission):
    """
    Check if user can approve a specific clearance record
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Only officers can approve/reject
        if request.user.role != 'OFFICER':
            return False
        
        # Check if officer belongs to this department
        if request.user not in obj.department.officers.all():
            return False
        
        # Check if record can be approved (stage order, etc.)
        return obj.can_approve()
