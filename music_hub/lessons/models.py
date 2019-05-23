from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.db import models


class Lessons(models.Model):
    title = models.CharField(max_length=255, unique=True)
    body = models.TextField()
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                              null=True)
    slug = models.SlugField(unique=True, null=True)

    class Meta:
        db_table = 'lessons'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Lessons, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} - {self.owner.name}'


class Likes(models.Model):
    liker = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                              related_name='likers', null=True)
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE,
                               related_name='likes', null=True)

    def __str__(self):
        return f'{self.liker} like {self.lesson}'
