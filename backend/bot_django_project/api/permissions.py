from rest_framework import permissions
from bots.models import Message, Variant


class IsBotOwnerOrForbidden(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Message):
            return obj.bot.owner == request.user
        elif isinstance(obj, Variant):
            return obj.current_message.bot.owner == request.user

    def has_permission(self, request, view):
        return request.user.is_authenticated
