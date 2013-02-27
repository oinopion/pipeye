from django.conf import settings
from django.db import models
from django.utils import timezone
from pipeye.accounts.models import MAILOUT_TIMES, User
from pipeye.packages.models import Package


class Watch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    package = models.ForeignKey('packages.Package')
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Watches'
        unique_together = ('user', 'package')

    def __unicode__(self):
        return "%s/%s" % (self.user.username, self.package.name)


def users_for_mailout(mailout_time):
    preferred_hour = max(h for h in MAILOUT_TIMES if h <= mailout_time.hour)
    last_mailout = models.F('last_mailout')
    qs = User.objects.all()
    qs = qs.filter(preferred_mailout_time=preferred_hour)
    qs = qs.filter(watch__package__changes__timestamp__gte=last_mailout)
    return qs.distinct()


def changed_for_user(user):
    qs = Package.objects.filter(watch__user=user)
    qs = qs.filter(changes__timestamp__gte=user.last_mailout)
    return qs.distinct().select_related('latest_version')

