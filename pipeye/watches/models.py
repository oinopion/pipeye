from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from pipeye.packages.models import Package


def mailout_choice(h):
    return (h, "%d:00-%d:00" % (h, h + MAILOUT_SPAN))
MAILOUT_SPAN = 3
MAILOUT_TIMES = range(0, 24, MAILOUT_SPAN)


class Watch(models.Model):
    user = models.ForeignKey('auth.User')
    package = models.ForeignKey('packages.Package')
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Watches'
        unique_together = ('user', 'package')

    def __unicode__(self):
        return "%s/%s" % (self.user.username, self.package.name)


class WatchSettings(models.Model):
    MAILOUT_CHOICES = [mailout_choice(h) for h in MAILOUT_TIMES]

    user = models.OneToOneField('auth.User')
    preferred_mailout_time = models.IntegerField(choices=MAILOUT_CHOICES)
    last_mailout = models.DateTimeField(default=timezone.now)


def users_for_mailout(mailout_time):
    preferred_hour = max(h for h in MAILOUT_TIMES if h <= mailout_time.hour)
    last_mailout = models.F('watchsettings__last_mailout')
    qs = User.objects.all()
    qs = qs.filter(watchsettings__preferred_mailout_time=preferred_hour)
    qs = qs.filter(watch__package__changes__timestamp__gte=last_mailout)
    return qs.distinct().select_related('watchsettings')


def changed_for_user(user):
    qs = Package.objects.filter(watch__user=user)
    qs = qs.filter(changes__timestamp__gte=user.watchsettings.last_mailout)
    return qs.distinct().select_related('latest_version')

