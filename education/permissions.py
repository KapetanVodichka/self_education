from rest_framework import permissions
from rest_framework.permissions import BasePermission
from users.models import User


class IsReadOnly(BasePermission):
    """
    Пользователь может выполнять только запросы на чтение (GET).
    Условно STUDENT.
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsTeacher(BasePermission):
    """
    Права на запросы выдаются пользователям с ролью TEACHER.
    """
    def has_permission(self, request, view):
        return request.user.role == User.TEACHER