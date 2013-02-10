import factory
from ..models import PackageRelease, Package, PackageReleaseChange

package_name_gen = lambda n: u'package-%s' % n
version_gen = lambda n: u'1.%s' % n


class PackageFactory(factory.Factory):
    FACTORY_FOR = Package
    name = factory.Sequence(package_name_gen)


class PackageReleaseDataFactory(factory.Factory):
    FACTORY_FOR = PackageRelease
    version = factory.Sequence(version_gen)
    summary = u'A package'
    home_page = u'http://example.com'
    package_url = u'http://example.com'
    release_url = u'http://example.com'
    author = u'Alice Doe'
    author_email = u'alice@example.com'
    maintainer = u''
    maintainer_email = u''


class PackageReleaseFactory(PackageReleaseDataFactory):
    package = factory.SubFactory(PackageFactory)


class PackageReleaseChangeFactory(factory.Factory):
    FACTORY_FOR = PackageReleaseChange
    package = factory.SubFactory(PackageFactory)

    @factory.lazy_attribute
    def release(change):
        return PackageReleaseFactory.create(package=change.package)

