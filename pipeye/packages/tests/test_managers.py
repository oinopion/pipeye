from django.test import TestCase
from expecter import expect
from ..models import Package, PackageRelease
from .factories import PackageReleaseDataFactory

class PackageManagerTest(TestCase):
    def test_all_package_names(self):
        names = ['a', 'b', 'c']
        Package.objects.create_from_names(names)
        expect(Package.objects.all_package_names()) == names

    def test_create_from_names(self):
        names = ['a', 'b', 'c']
        Package.objects.create_from_names(names)
        expect(Package.objects.filter(name__in=names).count()) == 3


class PackageReleasesManagerTest(TestCase):
    def setUp(self):
        self.package = Package.objects.create(name='abc')

    def test_create_from_release_data(self):
        data = [PackageReleaseDataFactory.attributes() for _ in range(3)]
        PackageRelease.objects.create_from_release_data(self.package, data)
        expect(self.package.releases.count()) == 3
