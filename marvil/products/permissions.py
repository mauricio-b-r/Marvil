from rest_framework import permissions

class ProductPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)

    def has_permission(self, request, view):
        # if request.method in permissions.SAFE_METHODS:
        #     # Check permissions for read-only request
        # else:
        #     # Check permissions for write request
        return super().has_permission(request, view)
