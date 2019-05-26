from django.contrib.auth import get_user_model
from django.db import models


class Subscribers(models.Model):
    subscriber = models.ForeignKey(get_user_model(),
                                   related_name='subscribers',
                                   on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name='followers',
                             on_delete=models.CASCADE)

    class Meta:
        unique_together = ('subscriber', 'user')

    def __str__(self):
        return f'{self.subscriber.name} subscribe {self.user.name}'
