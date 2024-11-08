from rest_framework.permissions import BasePermission
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Safe methods are allowed for everyone
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        # Only allow owners to edit
        return obj.owner == request.user