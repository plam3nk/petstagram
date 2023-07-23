# Send email on successful registration: Variant 3
# Best one
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from core.email_utils import send_email_with_template
from petstagram import settings

UserModel = get_user_model()


def send_successful_registration_email(user):
    context = {
        'user': user,
    }
    send_email_with_template(
        subject='Registration greetings',
        context=context,
        template_name='emails/email-greeting.html',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=(user.email, ),
    )

@receiver(post_save, sender=UserModel)
def user_created(instance, created, **kwargs):
    if created:
        send_successful_registration_email(instance)
