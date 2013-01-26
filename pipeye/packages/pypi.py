import xmlrpclib
from .models import Package, PackageRelease
from .forms import PackageReleaseForm


class Client(object):
    """Facade class encapsulating access to PyPI XML-RPC interface

    Docs available at http://wiki.python.org/moin/PyPiXmlRpc
    """
    PYPI_URL = 'http://pypi.python.org/pypi'

    def __init__(self):
        self.proxy = xmlrpclib.ServerProxy(self.PYPI_URL)

    def list_packages(self):
        """Returns list of strings with all package names"""
        return self.proxy.list_packages()

    def package_releases(self, package):
        """Returns list of strings with all releases of package"""
        return self.proxy.package_releases(package)

    def release_data(self, package, version):
        data = self.proxy.release_data(package, version)
        form = PackageReleaseForm(data)
        assert form.is_valid(), dict(form.data)
        return form.cleaned_data


class PackagesImporter(object):
    """Class encapsulating importing logic"""

    def __init__(self, client=None, manager=None):
        self.client = client or Client()
        self.manager = manager or Package.objects

    def all_packages(self):
        """Saves all packages names"""
        saved = self.manager.all_package_names()
        incoming = self.client.list_packages()
        names = missing(saved, incoming)
        self.manager.create_from_names(names)
        return len(names)


class ReleaseImporter(object):
    """Imports all releases for given package"""

    def __init__(self, client=None, manager=None):
        self.client = client or Client()
        self.manager = manager or PackageRelease.objects

    def package(self, package):
        saved_versions = package.versions()
        incoming_versions = self.client.package_releases(package.name)
        versions = missing(saved_versions, incoming_versions)
        data = [self.client.release_data(package.name, ver) for ver in versions]
        self.manager.create_from_release_data(package, data)
        return len(versions)


def missing(old, new):
    """Returns elements missing from old in comparison to new"""
    old = set(old)
    return [e for e in new if e not in old]
