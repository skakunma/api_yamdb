from rest_framework import permissions


class ThisAuthorOrReadOnly(permissions.BasePermission):
    """
    Класс ThisAuthorOrReadOnly.

    Класс ThisAuthorOrReadOnly описывает разрешение
    доступа к редактированию или удалению
    объекта только его автору. Запрос безопасных
    методов доступен всем.
    """

    def has_object_permission(self, request, view, obj):
        """
        Метод has_object_permission.

        Метод has_object_permission описывает разрешение
        для пользователей взаимодействовать (редактировать,
        удалять, просматривать) с определенным объектом.
        """
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role == 'admin'
            or request.user.role == 'moderator'
        )
