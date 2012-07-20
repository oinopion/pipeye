import mock
from mock import call
from expecter import expect
from unittest import TestCase
from ..pypi import Importer, missing

class ImporterTest(TestCase):
    def setUp(self):
        self.client = mock.Mock()
        self.manager = mock.Mock()
        self.importer = Importer(self.client, self.manager)


class AllPackagesImporterTest(ImporterTest):
    def test_saves_all_when_db_clean(self):
        self.client.list_packages.return_value = ['a', 'b', 'c']
        self.manager.all_package_names.return_value = []
        self.importer.all_packages()
        creates = self.manager.create.call_args_list
        expect(creates) == [call(name=n) for n in ['a', 'b', 'c']]

    def test_saves_nothing_when_db_same(self):
        self.client.list_packages.return_value = ['a', 'b', 'c']
        self.manager.all_package_names.return_value = ['a', 'b', 'c']
        self.importer.all_packages()
        creates = self.manager.create.call_args_list
        expect(creates) == []


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
