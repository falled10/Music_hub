from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Lessons
from .permissions import IsOwner
from .serializers import LessonsSerializer, LikesSerializer


class LessonsViewSet(ModelViewSet):
    serializer_class = LessonsSerializer
    queryset = Lessons.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwner
    ]

    @action(detail=True, methods=['GET'],
            permission_classes=[permissions.IsAuthenticated])
    def likes(self, request, pk=None):
        lesson = self.get_object()
        serializer = LikesSerializer(lesson.likes.all(), many=True)
        return Response(serializer.data)

    @likes.mapping.post
    def create_likes(self, request, pk=None):
        lesson = self.get_object()
        serializer = LikesSerializer(data=request.data)
        serializer.context['user'] = self.request.user
        serializer.context['lesson'] = lesson
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)