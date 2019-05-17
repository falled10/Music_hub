from django.db import models
from django.contrib.auth import get_user_model


class Lessons(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                 null=True)

    class Meta:
        db_table = 'lessons'

    def __str__(self):
        return f'{self.title} - {self.owner.name}'

class Likes(models.Model):
    liker = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, 
                                related_name='likers')
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCASE, 
                                related_name='likes')

    def __str__(self):
        return f'{self.liker} like {self.lesson}'
