from django.db import models
from django.utils import timezone

class PackageManager(models.Manager):
    def all_package_names(self):
        """Returns alphabetically sorted list of packages names"""
        return list(self.values_list('name', flat=True))

    def create_from_names(self, names):
        """Efficiently creates packages from list of names"""
        self.bulk_create([Package(name=name) for name in names])


class Package(models.Model):
    name = models.CharField(max_length=250, unique=True)
    objects = PackageManager()

    def __unicode__(self):
        return self.name

    def versions(self):
        return [rel.version for rel in self.releases.all()]


class PackageReleaseManager(models.Manager):
    def create_from_release_data(self, package, data):
        releases = [PackageRelease(package_id=package.id, **datum)
                    for datum in data]
        self.bulk_create(releases)


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