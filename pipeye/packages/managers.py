from django.db import models

class PackageReleaseManager(models.Manager):
    def create_from_release_data(self, package, data):
        releases = [self.model(package_id=package.id, **datum) for datum in data]
        self.bulk_create(releases)


class PackageManager(models.Manager):
    def all_package_names(self):
        """Returns alphabetically sorted list of packages names"""
        return list(self.values_list('name', flat=True))

    def create_from_names(self, names):
        """Efficiently creates packages from list of names"""
        self.bulk_create([self.model(name=name) for name in names])
