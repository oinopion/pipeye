import factory
from pipeye.accounts.tests.factories import UserFactory
from pipeye.packages.tests.factories import PackageFactory
from ..models import Watch


class WatchFactory(factory.Factory):
    FACTORY_FOR = Watch
    user = factory.SubFactory(UserFactory)
    package = factory.SubFactory(PackageFactory)
