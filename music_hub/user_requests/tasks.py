from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model


@shared_task
def notify_recipient(title, message, recipient_id, sender_id):
    sender = get_user_model().objects.get(id=sender_id)
    recipient = get_user_model().objects.get(id=recipient_id)
    mail_message = f'You have one request from {sender.email} - {message}'
    mail = EmailMultiAlternatives(title, mail_message, to=[recipient.email])
    mail.attach_alternative(mail_message, 'text/html')
    mail.send()
