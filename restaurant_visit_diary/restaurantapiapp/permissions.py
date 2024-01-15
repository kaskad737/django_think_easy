from rest_framework import permissions
from django.contrib.auth.models import User

# class IsOwnerOrReadOnly(permissions.BasePermission):

#     def has_permission(self, request, view):

#         if request.method in permissions.SAFE_METHODS:
#             return True
#         user = str(request.user).strip()
#         created_by = User.objects.filter(username=user)
#         if created_by:
#             t = str(created_by[0]).strip()
#             return t == user
#         else: 
#             return False

    # def has_object_permission(self, request, view, obj):
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #     print(obj.restaurant.created_by)
    #     print(request.user)
    #     return obj.restaurant.created_by == request.user
    #     return False
