from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Разрешение для проверки, является ли пользователь администратором.
    """

    def has_permission(self, request, view):
        # Проверка, аутентифицирован ли пользователь
        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.role == 'admin' or request.user.is_superuser
