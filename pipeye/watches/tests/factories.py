import factory
from pipeye.utils.factories import UserFactory
from pipeye.packages.tests.factories import PackageFactory
from ..models import Watch, WatchSettings


class WatchFactory(factory.Factory):
    FACTORY_FOR = Watch
    user = factory.SubFactory(UserFactory)
    package = factory.SubFactory(PackageFactory)


class WatchSettingsFactory(factory.Factory):
    FACTORY_FOR = WatchSettings
    user = factory.SubFactory(UserFactory)
    preferred_mailout_time = WatchSettings.MAILOUT_CHOICES[0]
