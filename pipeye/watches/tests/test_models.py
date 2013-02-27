from datetime import datetime, timedelta
from django.test import TestCase
from django.utils import timezone
from expecter import expect
from pipeye.accounts.tests.factories import UserFactory
from pipeye.packages.tests.factories import PackageFactory,\
    PackageReleaseFactory, PackageReleaseChangeFactory
from ..models import users_for_mailout, changed_for_user
from .factories import WatchFactory


class UserForMailoutTest(TestCase):
    mailout = timezone.make_aware(datetime(2013, 2, 7, 22), timezone.utc)

    def test_gets_users_for_specified_mailout_time(self):
        early = self.create_watching_user(preferred_mailout_time=0)
        late = self.create_watching_user(preferred_mailout_time=21)
        users = users_for_mailout(self.mailout)
        expect(users).does_not_contain(early)
        expect(users).contains(late)

    def test_gets_only_user_with_changed_packages(self):
        changed = self.create_watching_user()
        unchanged = self.create_watching_user(package=PackageFactory.create())
        users = users_for_mailout(self.mailout)
        expect(users).contains(changed)
        expect(users).does_not_contain(unchanged)

    def test_gets_only_users_with_changes_after_last_mailout(self):
        last_mailout = timezone.now() + timedelta(hours=1)
        mailed_recently = self.create_watching_user(last_mailout=last_mailout)
        users = users_for_mailout(self.mailout)
        expect(users).does_not_contain(mailed_recently)

    def test_gets_distinct_users(self):
        user = self.create_watching_user()
        WatchFactory.create(user=user, package=self.changed_package())
        users = users_for_mailout(self.mailout)
        expect(len(users)) == 1

    def changed_package(self):
        package = PackageFactory.create()
        package.latest_release = PackageReleaseFactory.create(package=package)
        package.save()
        return package

    def create_watching_user(self, last_mailout=None, preferred_mailout_time=21,
                             package=None):
        if not package:
            package = self.changed_package()
        if not last_mailout:
            last_mailout = self.mailout - timedelta(days=1)
        user = UserFactory.create(
            preferred_mailout_time=preferred_mailout_time,
            last_mailout=last_mailout
        )
        WatchFactory.create(user=user, package=package)
        return user


class ChangesForUserTest(TestCase):
    def setUp(self):
        self.user = UserFactory.create()

    def test_gets_user_watched_packages(self):
        watched = self.changed_package()
        not_watched = self.changed_package(watched=False)
        packages = changed_for_user(self.user)
        expect(packages).contains(watched)
        expect(packages).does_not_contain(not_watched)

    def test_gets_updated_packages(self):
        updated = self.changed_package()
        not_updated = PackageFactory.create()
        WatchFactory.create(user=self.user, package=not_updated)
        packages = changed_for_user(self.user)
        expect(packages).contains(updated)
        expect(packages).does_not_contain(not_updated)

    def test_gets_distinct_packages(self):
        package = self.changed_package()
        PackageReleaseChangeFactory.create(package=package)
        packages = changed_for_user(self.user)
        expect(len(packages)) == 1

    def changed_package(self, watched=True):
        package = PackageFactory.create()
        package.latest_release = PackageReleaseFactory.create(package=package)
        package.save()
        if watched:
            WatchFactory.create(user=self.user, package=package)
        return package
