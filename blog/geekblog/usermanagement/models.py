#-*- coding: UTF-8 -*-
import re
from uuid import uuid4
from django.db import models
from django.utils import timezone
from django.core import validators
from django.utils.translation import ugettext as _
from django.contrib.auth.models import Group, AbstractBaseUser, PermissionsMixin, BaseUserManager

from blogcore.utils import string_with_title
from blogcore.models.constants import USER_STATUS


class CustomGroup(Group):

    class Meta:
        proxy = True
        app_label = string_with_title('usermanagement', _('User Management'))
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')


class CustomUserManager(BaseUserManager):

    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = CustomUserManager.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=False, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.activation_code = uuid4().hex
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        u = self.create_user(username, email, password, **extra_fields)
        u.is_staff = True
        u.is_superuser = True
        u.status = USER_STATUS.ACTIVE
        u.save(using=self._db)
        return u


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(_('username'), max_length=50, unique=True,
        help_text=_('Required. 50 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), 'invalid')
        ])
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    status = models.IntegerField(default=0, choices=USER_STATUS.to_choices(), verbose_name=_('status'))
    qq = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('qq'))
    website = models.CharField(max_length=512, null=True, blank=True, verbose_name=_('website'))
    activation_code = models.CharField(max_length=255, blank=True, verbose_name=_('activation code'))

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __unicode__(self):
        return self.username

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """ Returns the short name for the user. """
        return self.first_name

    def save(self, *args, **kwargs):
        if not self.pk and not self.activation_code:
            self.activation_code = uuid4().hex
        super(CustomUser, self).save(*args, **kwargs)

    class Meta:
        app_label = string_with_title('usermanagement', _('User Management'))
        verbose_name = _('User')
        verbose_name_plural = _('Users')
