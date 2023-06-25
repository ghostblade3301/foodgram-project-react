from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or request.method == 'POST':
            return True
        elif (request.method in ['DELETE', 'PATCH'] and
              request.user == obj.author):
            return True
        return False