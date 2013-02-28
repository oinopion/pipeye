import factory
from pipeye.accounts.models import User

username_gen = lambda n: u'user_%s' % n
email_gen = lambda n: u'user-%s@example.com' % n


class UserFactory(factory.Factory):
    FACTORY_FOR = User
    username = factory.Sequence(username_gen)
    email = factory.Sequence(email_gen)
    preferred_mailout_time = 0

    @classmethod
    def _prepare(cls, create, **kwargs):
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        user.set_password(user.username)
        if create:
            user.save()
        return user
