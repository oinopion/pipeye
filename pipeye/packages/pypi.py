import time
import xmlrpclib
from .models import Package
from .forms import PackageForm, PackageReleaseForm


class PypiClient(object):
    """Facade class encapsulating access to PyPI XML-RPC interface

    Docs available at http://wiki.python.org/moin/PyPiXmlRpc
    """
    PYPI_URL = 'http://pypi.python.org/pypi'

    def __init__(self):
        self.proxy = xmlrpclib.ServerProxy(self.PYPI_URL)

    def list_packages(self):
        """Returns list of strings with all package names"""
        return self.proxy.list_packages()

    def package_releases(self, package_name):
        """Returns list of strings with all releases of package"""
        return self.proxy.package_releases(package_name)

    def release_data(self, package_name, version):
        """Returns dictionary with data for one release"""
        return self.proxy.release_data(package_name, version)

    def changelog(self, since):
        """Returns list of 4-tuples with PyPI changes"""
        return self.proxy.changelog(since)


class PackagesImporter(object):
    """Class encapsulating importing logic"""

    def __init__(self, client=None):
        self.client = client or PypiClient()

    def sync_all_packages(self):
        """Saves all packages names"""
        saved = Package.objects.all_package_names()
        incoming = self.client.list_packages()
        names = missing(saved, incoming)

        packages = []
        for name in names:
            form = PackageForm(data={'name': name})
            if form.is_valid():
                packages.append(form.save(commit=False))
        Package.objects.bulk_create(packages)
        return len(names)

    def sync_package(self, package):
        saved_versions = package.versions()
        incoming_versions = self.client.package_releases(package.name)
        versions = missing(saved_versions, incoming_versions)
        if not versions:
            return 0
        version_data = [self.client.release_data(package.name, version)
                for version in versions]

        releases = []
        for data in version_data:
            form = PackageReleaseForm(data=data)
            if form.is_valid():
                release = form.save(commit=False)
                release.package = package
                releases.append(release)
        package.releases.bulk_create(releases)
        package.latest_version = versions[0]
        package.save()
        return len(releases)

    def sync_changed(self, since):
        timestamp = datetime_to_time(since)
        changes = self.client.changelog(timestamp)
        new_packages = set()
        new_releases = set()
        for package_name, version, timestamp, action in changes:
            if action == 'create':
                new_packages.add(package_name)
            if action == 'new release':
                new_packages.add(package_name)
                new_releases.add(package_name)

        packages = []
        for name in new_packages:
            form = PackageForm(data={'name': name})
            if form.is_valid():
                packages.append(form.save(commit=False))
        Package.objects.bulk_create(packages)

        releases = 0
        for package_name in new_releases:
            package = Package.objects.get(name=package_name)
            releases += self.sync_package(package)

        return {'new_releases': releases, 'new_packages': len(packages)}


def missing(old, new):
    """Returns elements missing from old in comparison to new"""
    old = set(old)
    return [e for e in new if e not in old]

def datetime_to_time(dt):
    return int(time.mktime(dt.utctimetuple()))
