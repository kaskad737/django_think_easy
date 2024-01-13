from rest_framework import permissions

# class CustomPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # Allow authenticated users to create
#         if request.method == 'POST' and request.user.is_authenticated:
#             return True
#         # Add your custom logic for list view restrictions here
#         elif request.method == 'GET':
#             # Example: Allow only users with a specific attribute
#             return request.user.is_authenticated and request.user.has_some_attribute
#         return False