
from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnlyOrAuthenticated(BasePermission):
    '''
     GET, HEAD, OPTIONS — for all users.
    POST, PUT, PATCH, DELETE — only for authenticated users.
    '''
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user and request.user.is_authenticated


class IsOwnerOrAdminOrReadOnly(BasePermission):
    '''
     GET, HEAD, OPTIONS — for all users.
    POST, PUT, PATCH, DELETE — only for owner or admin.
    '''
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user or request.user.is_superuser