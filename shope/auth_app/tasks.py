from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from shope.celery import app


@app.task
def send_mail_to_user(subject, message, email):
    return send_mail(
        subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False
    )
