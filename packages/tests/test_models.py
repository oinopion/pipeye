from django.test import TestCase
from expecter import expect
from ..models import Package

class PackageManagerTest(TestCase):
    def test_all_package_names(self):
        names = ['a', 'b', 'c']
        Package.objects.create_from_names(names)
        expect(Package.objects.all_package_names()) == names

    def test_create_from_names(self):
        names = ['a', 'b', 'c']
        Package.objects.create_from_names(names)
        expect(Package.objects.filter(name__in=names).count()) == 3
