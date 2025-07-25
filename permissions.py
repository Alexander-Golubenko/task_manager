from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnlyOrAuthenticated(BasePermission):
    '''
     GET, HEAD, OPTIONS — for all users.
    POST, PUT, PATCH, DELETE — only for authenticated users.
    '''
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user and request.user.is_authenticated