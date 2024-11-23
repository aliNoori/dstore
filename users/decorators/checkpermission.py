from rest_framework.response import Response
from rest_framework import status

class PermissionMixin:
    required_permission = None

    def check_permission(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        if not self.required_permission:
            return None
        if not request.user.has_perm(self.required_permission):
            return Response({'detail': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        return None
