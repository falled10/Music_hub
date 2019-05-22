import logging

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model


@shared_task
def send_verification_email(user_id):
    UserModel = get_user_model()
    try:
        user = get_user_model().objects.filter(id=user_id)
        user = user.first()
        link = f'http://localhost:3000/#/verify/{user.verification_uuid}'
        title = 'Verify your Music Hub account'
        mail_message = f'Follow this link to verify your account {link}'
        mail = EmailMultiAlternatives(title, mail_message, to=[user.email])
        mail.attach_alternative(mail_message, 'text/html')
        mail.send()
    except get_user_model().DoesNotExist:
        logging.warning('Tried to send verification email to non-existing user')
