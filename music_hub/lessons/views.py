from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .models import Lessons
from .permissions import IsOwnerOrReadOnly
from .serializers import LessonsSerializer, LikesSerializer
from .pagination import LessonsPagination


class LessonsViewSet(ModelViewSet):
    """
    list:
    Get list of all views
    ## Markdown
    ```json
    {
        "id": 1
        "title": "something",
        "body": "something",
        "owner": {
            "id": 1,
            "email": "something@gmail.com",
            "name": "Something",
            "image": "something"
        }
    },
    ...
    ```
    retrieve:
    Get one lesson

    create:
    Create one lesson

    update:
    Update one Lesson

    likes:
    Get likes of one lesson by slug.
    """
    serializer_class = LessonsSerializer
    queryset = Lessons.objects.all()
    lookup_field = 'slug'
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    pagination_class = LessonsPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('title', 'owner')

    @action(detail=True, methods=['GET'],
            permission_classes=[permissions.IsAuthenticated])
    def likes(self, request, slug=None):
        """
        Return likes for lesson by slug
        """
        lesson = self.get_object()
        serializer = LikesSerializer(lesson.likes.all(), many=True)
        return Response(serializer.data)

    @likes.mapping.post
    def create_likes(self, request, slug=None):
        """
        Check if there is exists like same as we want create
        then delete this like, else create like
        """
        lesson = self.get_object()
        serializer = LikesSerializer(data=request.data)
        serializer.context['user'] = self.request.user
        serializer.context['lesson'] = lesson
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if None in serializer.data.values():
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
