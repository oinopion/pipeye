from django.db import models
from django.utils import timezone


class Watch(models.Model):
    user = models.ForeignKey('auth.User')
    package = models.ForeignKey('packages.Package')
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Watches'

    def __unicode__(self):
        return "%s/%s" % (self.user.username, self.package.name)
