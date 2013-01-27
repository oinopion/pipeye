import factory
from ..models import PackageRelease

version_gen = lambda n: u'1.%s' % n

class PackageReleaseFactory(factory.Factory):
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
