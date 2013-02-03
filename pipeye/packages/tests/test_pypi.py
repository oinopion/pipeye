import mock
import unittest
from expecter import expect
from ..pypi import PackagesImporter, ReleaseImporter, missing

class ImporterTest(unittest.TestCase):
    def setUp(self):
        self.client = mock.Mock()
        self.manager = mock.Mock()
        self.importer = PackagesImporter(self.client, self.manager)
        self.names = ['a', 'b', 'c']
        self.client.list_packages.return_value = self.names

    def test_saves_all_when_db_clean(self):
        self.manager.all_package_names.return_value = []
        self.importer.all_packages()
        self.manager.create_from_names.assert_called_with(self.names)

    def test_saves_nothing_when_db_same(self):
        self.manager.all_package_names.return_value = self.names
        self.importer.all_packages()
        self.manager.create_from_names.assert_called_with([])

    def test_returns_number_of_packages_added(self):
        self.manager.all_package_names.return_value = ['b']
        expect(self.importer.all_packages()) == 2


class PackageReleasesImporterTest(unittest.TestCase):
    def setUp(self):
        self.client = mock.Mock()
        self.manager = mock.Mock()
        self.importer = ReleaseImporter(self.client, self.manager)
        self.releases = ['2.0', '1.2', '1.1']
        self.release_data = mock.Mock(name='data')
        self.client.package_releases.return_value = self.releases
        self.client.release_data.return_value = self.release_data
        self.package = mock.Mock()
        self.package.name = 'abc'

    def test_fetches_all_releases_when_empty(self):
        self.package.versions.return_value = []
        self.importer.package(self.package)
        self.manager.create_from_release_data.assert_called_with(
            self.package, [self.release_data] * 3)

    def test_fetches_none_if_releases_same(self):
        self.package.versions.return_value = self.releases
        self.importer.package(self.package)
        self.manager.create_from_release_data.assert_called_with(
            self.package, [])

    def test_sets_latest_version(self):
        self.package.versions.return_value = []
        self.importer.package(self.package)
        expect(self.package.latest_version) == self.releases[0]
        self.package.save.assert_called_with()

    def test_does_not_set_latest_version_if_not_versions(self):
        self.package.versions.return_value = []
        self.client.package_releases.return_value = []
        self.importer.package(self.package)
        expect(self.package.latest_version.called) == False
        expect(self.package.save.called) == False

    def test_returns_number_of_fetched_vesrions(self):
        self.package.versions.return_value = self.releases[0:1]
        expect(self.importer.package(self.package)) == 2


class MissingTest(unittest.TestCase):
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
