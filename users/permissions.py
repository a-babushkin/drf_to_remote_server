from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """Проверяет, является ли текущий пользователь членом группы Модераторы"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Модераторы").exists()


class IsOwner(permissions.BasePermission):
    """Проверяет, является ли текущий пользователь владельцем"""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
