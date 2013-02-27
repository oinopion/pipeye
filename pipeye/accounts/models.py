from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils import timezone

MAILOUT_SPAN = 3
MAILOUT_TIMES = range(0, 24, MAILOUT_SPAN)


def mailout_choice(h):
    return (h, "%d:00-%d:00" % (h, h + MAILOUT_SPAN))


class User(PermissionsMixin, AbstractBaseUser):
    MAILOUT_CHOICES = [mailout_choice(h) for h in MAILOUT_TIMES]
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    username = models.CharField(max_length=250, unique=True)
    email = models.EmailField(max_length=250)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_mailout = models.DateTimeField(default=timezone.now)
    preferred_mailout_time = models.IntegerField(choices=MAILOUT_CHOICES,
                                                 default=MAILOUT_CHOICES[0][0])

    objects = UserManager()

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.username
