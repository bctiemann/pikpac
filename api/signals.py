from django.conf import settings
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import ugettext_lazy as _


@receiver(reset_password_token_created)
#def password_reset_token_created(*args, **kwargs):
def password_reset_token_created(sender=None, instance=None, reset_password_token=None, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'site_name': settings.SITE_NAME,
        'server_base_url': settings.FRONTEND_BASE_URL,
        'reset_url': '/auth/reset-password/',
        # 'current_user': reset_password_token.user,
        'email': reset_password_token.user.email,
        'token': reset_password_token.key,
        # 'reset_password_url': "{}?token={}".format(reverse('api:password_reset:reset-password-confirm'), reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        _("Password Reset for {title}".format(title=settings.SITE_NAME)),
        # message:
        email_plaintext_message,
        # from:
        settings.NOTIFICATION_SENDER_EMAIL,
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()