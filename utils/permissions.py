from rest_framework.permissions import BasePermission, SAFE_METHODS

# class IsOwnerOrReadOnly(BasePermission):
#     def has_object_permission(self, request, view,obj):
#         if request.method in SAFE_METHODS:
#             return True
        
#         return obj.owner ==request.user

class IsOwnerOrShared (BasePermission):
    def has_edit_permission(self, request, view, basket):
        return request.user in basket.shared_with