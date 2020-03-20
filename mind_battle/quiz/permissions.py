from rest_framework.permissions import BasePermission
from rest_framework.permissions


class IsCreator(BasePermission):
    """Permission that check if request.user is creator"""

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user
