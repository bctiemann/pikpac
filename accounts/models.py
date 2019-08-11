import uuid
import urllib

from django.conf import settings
from django.core import mail
from django.db import models
from django.contrib.auth.models import BaseUserManager, UserManager, AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import six, timezone
from django.template.loader import get_template

from rest_framework.authentication import TokenAuthentication

from phonenumber_field.modelfields import PhoneNumberField

import logging
logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=191,
        unique=True,
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_admin = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    confirm_hashkey = models.CharField(null=True, blank=True, max_length=40, unique=True)
    confirm_sent = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    eula_accepted = models.DateTimeField(null=True, blank=True)
    deleted = models.DateTimeField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = PhoneNumberField(blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    stripe_customer = models.CharField(null=True, blank=True, max_length=30)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def send_confirm(self):
        self.confirm_hashkey = uuid.uuid4().hex
        self.confirm_sent = timezone.now()
        self.save()

        text_template = get_template('email/signup_confirm.txt')
        html_template = get_template('email/signup_confirm.html')
        context = {
            'site_name': settings.SITE_NAME,
            'server_base_url': settings.FRONTEND_BASE_URL,
            'confirm_url': '/auth/register-confirm/',
            'email': urllib.parse.quote_plus(self.email),
            'confirm_hashkey': self.confirm_hashkey,
        }

        subject = 'Pikpac account confirmation'
        text_content = text_template.render(context)
        html_content = html_template.render(context)

        recipients = [self.email]
        bcc = []

        for admin, admin_email in settings.ADMINS:
            bcc.append(admin_email)

        msg = mail.EmailMultiAlternatives(subject, text_content, settings.NOTIFICATION_SENDER_EMAIL, recipients, bcc)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        logger.info('Sending confirmation email to {0}'.format(self.email))

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_still_confirmable(self):
        return (timezone.now() - self.confirm_sent).total_seconds() < settings.SIGNUP_CONFIRM_TIMEOUT_DAYS * 86400

    @property
    def eula_current(self):
        eula_date = datetime.strptime(settings.EULA_DATE,'%Y-%m-%d')
        return self.eula_accepted != None and (eula_date < self.eula_accepted.replace(tzinfo=None))

    @property
    def is_deleted(self):
        if self.deleted == None:
            return False
        return (timezone.now() - self.deleted).total_seconds() > settings.ACCOUNT_DELETE_GRACE_DAYS * 86400

    @property
    def is_deleted_grace(self):
        if self.deleted == None:
            return False
        return self.deleted and (timezone.now() - self.deleted).total_seconds() < settings.ACCOUNT_DELETE_GRACE_DAYS * 86400


class BearerTokenAuthentication(TokenAuthentication):

    keyword = 'Bearer'
