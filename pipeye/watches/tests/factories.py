import factory
from pipeye.accounts.factories import UserFactory
from pipeye.packages.tests.factories import PackageFactory
from ..models import Watch


class WatchFactory(factory.Factory):
    FACTORY_FOR = Watch
    user = factory.SubFactory(UserFactory)
    package = factory.SubFactory(PackageFactory)
