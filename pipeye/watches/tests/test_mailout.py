from datetime import datetime
from django.core import mail
from django.test import TestCase
from django.utils import timezone
from expecter import expect
from pipeye.accounts.factories import UserFactory
from pipeye.accounts.models import User
from pipeye.packages.tests.factories import PackageFactory
from ..mailout import Mailout


class MailoutTest(TestCase):
    def setUp(self):
        self.mailout_time = timezone.utc.fromutc(datetime(2012, 1, 1, 13, 45))
        self.manager = FakeManager()
        self.mailout = Mailout(self.mailout_time, manager=self.manager)

    def test_sends_email_to_each_indicated_user(self):
        self.mailout.send()
        expect(len(mail.outbox)) == len(self.manager.users)

    def test_saves_last_mailout_time(self):
        self.mailout.send()
        for user in self.manager.users:
            expect(user.last_mailout) == self.mailout_time


class FakeManager(object):
    def __init__(self):
        self.users = UserFactory.create_batch(2)
        self.changed_packages = PackageFactory.build_batch(3)

    def users_for_mailout(self, mailout_time):
        expect(mailout_time).isinstance(datetime)
        return self.users

    def changed_for_user(self, user):
        expect(user).isinstance(User)
        return self.changed_packages
