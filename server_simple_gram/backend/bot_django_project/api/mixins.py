from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin


class RetrieveUpdateDestroyViewSet(RetrieveModelMixin, UpdateModelMixin,
                                   DestroyModelMixin, GenericViewSet):
    pass