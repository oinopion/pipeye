import factory
from django.contrib.auth.models import User

username_gen = lambda n: u'user_%s' % n

class UserFactory(factory.Factory):
    """Creates auth.User with password same as username"""
    FACTORY_FOR = User
    username = factory.Sequence(username_gen)

    @classmethod
    def _prepare(cls, create, **kwargs):
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        user.set_password(user.username)
        if create:
            user.save()
        return user
