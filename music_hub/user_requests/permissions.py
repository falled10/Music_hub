from rest_framework.permissions import BasePermission


class IsSenderOrRecipient(BasePermission):

    def has_object_permission(self, request, view, obj):
        """ Can Read or create only sender or recipient
        """
        return request.user == obj.sender or request.user == obj.recipient
