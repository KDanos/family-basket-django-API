from rest_framework.permissions import BasePermission

class IsOwnerOrShared (BasePermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view)
    
    def has_object_permission(self, request, view, basket):
        if request.method == 'DELETE': 
            return request.user == basket.owner
        return request.user in basket.shared_with.all() or request.user == basket.owner