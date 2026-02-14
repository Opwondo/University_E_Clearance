from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Permission for administrators only
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'

class IsOfficer(permissions.BasePermission):
    """
    Permission for department officers
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'OFFICER'

class IsStudent(permissions.BasePermission):
    """
    Permission for students only
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'STUDENT'

class IsStudentOrReadOnly(permissions.BasePermission):
    """
    Students can only access their own data, others can read
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the student themselves
        return hasattr(obj, 'user') and obj.user == request.user

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to allow owners or admins to edit
    """
    def has_object_permission(self, request, view, obj):
        # Admins have full access
        if request.user.role == 'ADMIN':
            return True
        
        # Check if the user is the owner
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'student'):
            return obj.student.user == request.user
        
        return False
