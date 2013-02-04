import mock
from django.utils import timezone
from django.test import TestCase
from expecter import expect
from ..models import Package
from ..pypi import PackagesImporter, missing, PypiClient
from .factories import PackageFactory


class BaseImporterTest(TestCase):
    def setUp(self):
        self.client = PypiClient()
        self.client.proxy = StubProxy()
        self.importer = PackagesImporter(self.client)


class ImporterAllPackagesTest(BaseImporterTest):
    def test_saves_all(self):
        self.importer.sync_all_packages()
        all_names = set(Package.objects.all_package_names())
        expect(all_names) == set(self.client.list_packages())

    def test_returns_number_of_packages_added(self):
        expect(self.importer.sync_all_packages()) == len(self.client.list_packages())


class ImporterPackageSyncTest(BaseImporterTest):
    def setUp(self):
        super(ImporterPackageSyncTest, self).setUp()
        self.package = PackageFactory.create()

    def test_fetches_all_releases(self):
        self.importer.sync_package(self.package)
        versions = set(self.package.versions())
        expect(versions) == set(self.client.package_releases(''))

    def test_sets_latest_version(self):
        self.importer.sync_package(self.package)
        expect(self.package.latest_version) == self.client.package_releases('')[0]

    def test_does_not_set_latest_version_if_not_versions(self):
        self.client.proxy.package_releases = mock.Mock(return_value=[])
        self.importer.sync_package(self.package)
        expect(self.package.latest_version) == ''

    def test_returns_number_of_fetched_versions(self):
        imported = self.importer.sync_package(self.package)
        expect(imported) == len(self.client.package_releases(''))


class ImporterSyncChangedTest(BaseImporterTest):
    def setUp(self):
        super(ImporterSyncChangedTest, self).setUp()

    def test_imports_package_releases_on_new_release(self):
        spam = PackageFactory.create(name='spam')
        self.importer.sync_changed(timezone.now())
        expect(set(spam.versions())) == set(self.client.package_releases(''))

    def test_imports_package_on_create(self):
        self.importer.sync_changed(timezone.now())
        expect(Package.objects.filter(name='bacon').exists()) == True

    def test_returns_number_of_packages_and_releases(self):
        result = self.importer.sync_changed(timezone.now())
        expect(result['new_releases']) == 8


class MissingTest(TestCase):
    def test_exclusive(self):
        old = [1, 2]
        new = [3, 4]
        expect(missing(old, new)) == [3, 4]

    def test_same(self):
        old = [1, 2]
        new = [1, 2]
        expect(missing(old, new)) == []

    def test_missing_end(self):
        old = [1, 2]
        new = [2, 3]
        expect(missing(old, new)) == [3]

    def test_missing_beginning(self):
        old = [2, 3]
        new = [1, 2]
        expect(missing(old, new)) == [1]

    def test_missing_middle(self):
        old = [1, 3]
        new = [1, 2, 3]
        expect(missing(old, new)) == [2]


class StubProxy(object):
    def list_packages(self):
        return ['bacon', 'spam', 'eggs']

    def package_releases(self, package):
        expect(package).isinstance(basestring)
        return ['1.5', '1.0', '0.9', '0.5']

    def release_data(self, package, version):
        expect(package).isinstance(basestring)
        expect(version).isinstance(basestring)
        return {
            'name': package,
            'version': version,
            'summary': 'This is awesome package',
            'home_page': 'http://www.%s.com/' % package,
            'package_url': 'http://example.org/pypi/%s' % package,
            'release_url': 'http://example.org/pypi/%s/%s' % (package, version),
            'author': 'Team %s' % package,
            'author_email': 'team@example.com',
        }

    def changelog(self, since):
        expect(since).isinstance(int)
        return [
            ['bacon', '0.1', since + 14, 'new release'],
            ['bacon', None, since + 14, 'create'],
            ['spam', '2.1', since + 10, 'new release'],
            ['cheese', '0.1', since + 4, 'remove'],
        ]
