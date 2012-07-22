from django.test import TestCase
from expecter import expect
from ..models import Package

class PackageManagerTest(TestCase):
    def test_all_package_names(self):
        names = ['a', 'b', 'c']
        for n in names:
            Package.objects.create(name=n)
        expect(Package.objects.all_package_names()) == names
