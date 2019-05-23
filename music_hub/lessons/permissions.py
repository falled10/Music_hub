from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        """ Get permission to read if user is not owner,
        and for delete and update if user is owner
        """
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.owner
