from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_task(user, email):
    send_mail(
            subject='Password Reset',
            message=f'Dear {user}',
            from_email='django_test_email',
            recipient_list=[email]
            )
