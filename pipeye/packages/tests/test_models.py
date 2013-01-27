from django.test import TestCase
from expecter import expect
from ..models import Package
from .factories import PackageReleaseFactory


class PackageTest(TestCase):
    def setUp(self):
        self.package = Package.objects.create(name='abc')

    def test_versions_of_fresh(self):
        expect(self.package.versions()) == []

    def test_versions_of_older(self):
        releases = PackageReleaseFactory.create_batch(3, package=self.package)
        versions = [rel.version for rel in releases]
        expect(set(self.package.versions())) == set(versions)

