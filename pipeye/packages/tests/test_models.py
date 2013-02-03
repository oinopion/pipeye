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

    def test_latest_version_of_fresh(self):
        expect(self.package.latest_version) == ''

    def test_latest_version_of_older(self):
        release = PackageReleaseFactory.create(package=self.package)
        self.package.latest_release = release
        expect(self.package.latest_version) == release.version

    def test_settings_latest_version(self):
        release = PackageReleaseFactory.create(package=self.package)
        self.package.latest_version = release.version
        expect(self.package.latest_release) == release
