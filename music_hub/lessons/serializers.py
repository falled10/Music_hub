from django.db import transaction
from rest_framework import serializers

from authorization.serializers import UserSerializer
from .models import Lessons, Likes


class LikesSerializer(serializers.ModelSerializer):
    liker = UserSerializer(read_only=True)

    class Meta:
        model = Likes
        fields = ('liker', 'lesson')

    def validate(self, attrs):
        attrs['liker'] = self.context['user']
        attrs['lesson'] = self.context['lesson']
        return super().validate(attrs)

    def create(self, validated_data):
        lesson = validated_data['lesson']
        user = validated_data['liker']
        like = Likes.objects.filter(liker=user, lesson=lesson)
        with transaction.atomic():
            if like.exists():
                like.delete()
                return like
        return Likes.objects.create(liker=user, lesson=lesson)


class LessonsSerializer(serializers.ModelSerializer):
    likes = LikesSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)

    lookup_field = 'slug'

    class Meta:
        model = Lessons
        fields = ('title', 'body', 'owner', 'slug', 'likes')
