from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from bots.models import Message, Variant, Bot, Command


class IsMessageOwnerOrForbidden(permissions.BasePermission):
    """
    Проверка получения доступа к объекту Message.
    Разрешены сообщения только для своего бота.
    """
    def has_object_permission(self, request: Request, view: ModelViewSet, obj: Message) -> bool:
        return obj.bot.owner == request.user

    def has_permission(self, request: Request, view: ModelViewSet) -> bool:
        return request.user.is_authenticated


class IsVariantOwnerOrForbidden(permissions.BasePermission):
    """
    Проверка получения доступа к объекту Variant.
    Разрешены варианты только для своего бота.
    """
    def has_object_permission(self, request: Request, view: ModelViewSet, obj: Variant) -> bool:
        return obj.current_message.bot.owner == request.user

    def has_permission(self, request: Request, view: ModelViewSet) -> bool:
        return request.user.is_authenticated


class IsBotOwnerOrForbidden(permissions.BasePermission):
    """
    Проверка получения доступа к объекту Bot.
    Разрешен доступ только для своего бота.
    """
    def has_object_permission(self, request: Request, view: ModelViewSet, obj: Bot) -> bool:
        return obj.owner == request.user

    def has_permission(self, request: Request, view: ModelViewSet) -> bool:
        return request.user.is_authenticated and all(bot.owner == request.user for bot in view.get_queryset())


class IsCommandOwnerOrForbidden(permissions.BasePermission):
    """
    Проверка получения доступа к объекту Command.
    Разрешен доступ к командам только для своего бота.
    """
    def has_object_permission(self, request: Request, view: ModelViewSet, obj: Command) -> bool:
        return obj.bot.owner == request.user

    def has_permission(self, request: Request, view: ModelViewSet) -> bool:
        return request.user.is_authenticated
