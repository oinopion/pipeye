from django.test import TestCase
from expecter import expect
from ..models import Package, PackageRelease
from .factories import PackageReleaseFactory

class PackageManagerTest(TestCase):
    def test_all_package_names(self):
        names = ['a', 'b', 'c']
        Package.objects.create_from_names(names)
        expect(Package.objects.all_package_names()) == names

    def test_create_from_names(self):
        names = ['a', 'b', 'c']
        Package.objects.create_from_names(names)
        expect(Package.objects.filter(name__in=names).count()) == 3


class PackageTest(TestCase):
    def setUp(self):
        self.package = Package.objects.create(name='abc')

    def test_versions_of_fresh(self):
        expect(self.package.versions()) == []

    def test_versions_of_older(self):
        releases = PackageReleaseFactory.create_batch(3, package=self.package)
        versions = [rel.version for rel in releases]
        expect(set(self.package.versions())) == set(versions)


class PackageReleasesManagerTest(TestCase):
    def setUp(self):
        self.package = Package.objects.create(name='abc')

    def test_create_from_release_data(self):
        data = [PackageReleaseFactory.attributes() for _ in range(3)]
        PackageRelease.objects.create_from_release_data(self.package, data)
        expect(self.package.releases.count()) == 3
