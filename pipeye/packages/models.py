from django.db import models
from django.utils import timezone
from .managers import PackageReleaseManager, PackageManager


class Package(models.Model):
    name = models.CharField(max_length=250, unique=True)
    objects = PackageManager()

    def __unicode__(self):
        return self.name

    def versions(self):
        return [rel.version for rel in self.releases.all()]


class PackageRelease(models.Model):
    package = models.ForeignKey(Package, related_name='releases')
    version = models.CharField(max_length=100)
    summary = models.TextField(blank=True)
    home_page = models.TextField(blank=True)
    package_url = models.TextField(blank=True)
    release_url = models.TextField(blank=True)
    author = models.TextField(blank=True)
    author_email = models.TextField(blank=True)
    maintainer = models.TextField(blank=True)
    maintainer_email = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    objects = PackageReleaseManager()

    class Meta:
        unique_together = ('version', 'package')

    def __unicode__(self):
        return "%s-%s" % (self.package.name, self.version)
