from django.db import models
from django.utils import timezone
from .managers import PackageReleaseManager, PackageManager


class Package(models.Model):
    name = models.CharField(max_length=250, unique=True)
    latest_release = models.ForeignKey('PackageRelease', related_name='+',
        null=True, blank=True)
    objects = PackageManager()

    class Meta:
        ordering = ('name',)

    def __init__(self, *args, **kwargs):
        super(Package, self).__init__(*args, **kwargs)
        self.__previous_latest_release_id = self.latest_release_id

    def __unicode__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None):
        super(Package, self).save(force_insert, force_update, using)
        if self.latest_release_changed:
            self.changes.create(release=self.latest_release)

    def versions(self):
        return [rel.version for rel in self.releases.all()]

    @property
    def latest_release_changed(self):
        return self.latest_release_id != self.__previous_latest_release_id

    @property
    def latest_version(self):
        if self.latest_release:
            return self.latest_release.version
        return ''

    @latest_version.setter
    def latest_version(self, new_version):
        self.latest_release = self.releases.get(version=new_version)


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


class PackageReleaseChange(models.Model):
    package = models.ForeignKey(Package, related_name='changes')
    release = models.ForeignKey(PackageRelease, related_name='+')
    timestamp = models.DateTimeField(default=timezone.now)


class PackageImport(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
