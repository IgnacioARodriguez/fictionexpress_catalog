from rest_framework import permissions
"""
Custom permission to only allow editors to edit objects.
Read-only access is allowed for any request.
Methods:
    has_permission(request, view): Checks if the user has permission to perform the action.
"""

class IsEditorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True

        return request.user.is_authenticated and request.user.role == 'editor'
