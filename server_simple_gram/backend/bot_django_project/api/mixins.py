from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin


class RetrieveUpdateDestroyViewSet(RetrieveModelMixin, UpdateModelMixin,
                                   DestroyModelMixin, GenericViewSet):
    pass


class ListPostViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    pass
