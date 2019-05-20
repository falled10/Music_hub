from django.contrib.auth import get_user_model
from django.db import models

from .tasks import notify_recipient


class Requests(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                               null=True, related_name='senders')
    recipient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                  related_name='recipients')

    class Meta:
        db_table = 'requests'

    def __str__(self):
        return f'{self.sender.name}`s request with {self.title} title'


def request_post_save(sender, instance, signal, *args, **kwargs):
    notify_recipient.delay(instance.title, instance.body,
                           instance.recipient.id,
                           instance.sender.id)


models.signals.post_save.connect(request_post_save, sender=Requests)
