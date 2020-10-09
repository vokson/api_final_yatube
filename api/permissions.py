from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS
