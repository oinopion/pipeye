import time
import logging
import xmlrpclib
from .models import Package
from .forms import PackageForm, PackageReleaseForm

logger = logging.getLogger(__name__)


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

    def missing_packages(self, known):
        incoming = self.list_packages()
        return missing(known, incoming)

    def missing_version_data(self, package_name, known_versions):
        incoming_versions = self.package_releases(package_name)
        versions = missing(known_versions, incoming_versions)
        if not versions:
            return {}
        logging.debug('Fetching %d releases of %s', len(versions), package_name)
        versions_data = [self.release_data(package_name, v) for v in versions]
        return {
            'missing_versions': versions_data,
            'latest_version': incoming_versions[0],
        }

    def changes(self, since):
        logging.info('Syncing packages since: %s', since)
        timestamp = datetime_to_time(since)
        changes = self.changelog(timestamp)
        new_packages = set()
        new_releases = set()
        for package_name, version, timestamp, action in changes:
            if action == 'create':
                new_packages.add(package_name)
            if action == 'new release':
                new_packages.add(package_name)
                new_releases.add(package_name)
        logging.info('New packages: %d', len(new_packages))
        logging.info('Packages with new releases: %d', len(new_releases))
        return {'new_packages': new_packages, 'new_releases': new_releases}


class PackagesImporter(object):
    """Class encapsulating importing logic"""

    def __init__(self, client=None):
        self.client = client or PypiClient()

    def sync_all_packages(self):
        """Saves all packages names"""
        saved = Package.objects.all_package_names()
        names = self.client.missing_packages(saved)
        return self._create_packages(names)

    def sync_package(self, package):
        known = package.versions()
        version_data = self.client.missing_version_data(package.name, known)
        return self._save_package_releases(package, version_data)

    def sync_changed(self, since):
        changes = self.client.changes(since)
        packages_created = self._create_packages(changes['new_packages'])
        packages = Package.objects.filter(name__in=changes['new_releases'])
        releases = 0
        for package in packages:
            releases += self.sync_package(package)
        return {'new_releases': releases, 'new_packages': packages_created}

    def _create_packages(self, names):
        packages = []
        for name in names:
            form = PackageForm(data={'name': name})
            if form.is_valid():
                packages.append(form.save(commit=False))
        Package.objects.bulk_create(packages)
        return len(names)

    def _save_package_releases(self, package, version_data):
        if not version_data:
            return 0
        missing_versions = version_data['missing_versions']
        releases = []
        for data in missing_versions:
            form = PackageReleaseForm(data=data)
            if form.is_valid():
                release = form.save(commit=False)
                release.package = package
                releases.append(release)
        package.releases.bulk_create(releases)
        package.latest_version = version_data['latest_version']
        package.save()
        return len(releases)


def missing(old, new):
    """Returns elements missing from old in comparison to new"""
    old = set(old)
    return [e for e in new if e not in old]

def datetime_to_time(dt):
    return int(time.mktime(dt.utctimetuple()))
