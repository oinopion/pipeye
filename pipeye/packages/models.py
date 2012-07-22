from django.db import models

class PackageManager(models.Manager):
    def all_package_names(self):
        """Returns alphabetically sorted list of packages names"""
        return list(self.values_list('name', flat=True))


class Package(models.Model):
    name = models.CharField(max_length=250, unique=True)
    objects = PackageManager()

    def __unicode__(self):
        return self.name


class PackageRelease(models.Model):
    package = models.ForeignKey(Package)
    version = models.CharField(max_length=100)
    summary = models.TextField()
    home_page = models.URLField()
    package_url = models.URLField()
    release_url = models.URLField()
    author = models.TextField()
    author_email = models.EmailField()
    maintainer = models.TextField()
    maintainer_email = models.EmailField()
    timestamp = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('version', 'package')

    def __unicode__(self):
        return "%s: %s" % (self.package.name, self.version)
