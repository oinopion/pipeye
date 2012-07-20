import xmlrpclib
from .models import Package, PackageRelease


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
        return self.proxy.release_data(package, version)


class Importer(object):
    """Class encapsulating importing logic"""

    def __init__(self, client, manager):
        self.client = client
        self.manager = manager

    def all_packages(self):
        """Saves all packages names"""
        saved = self.manager.all_package_names()
        incoming = self.client.list_packages()
        for package in missing(saved, incoming):
            self.manager.create(name=package)


def missing(old, new):
    old = set(old)
    return [e for e in new if e not in old]
