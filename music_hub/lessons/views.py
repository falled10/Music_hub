from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from .serializers import LessonsSerializer
from .models import Lessons
from .permissions import IsOwner


class LessonsViewSet(ModelViewSet):
    serializer_class = LessonsSerializer
    queryset = Lessons.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwner
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
