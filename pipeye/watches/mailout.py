from django.template.loader import render_to_string
from .models import users_for_mailout, changed_for_user


class MailoutManager(object):
    def users_for_mailout(self, mailout_time):
        return users_for_mailout(mailout_time)

    def changed_for_user(self, user):
        return changed_for_user(user)


class Mailout(object):
    def __init__(self, mailout_time, manager=None):
        self.mailout_time = mailout_time
        self.manager = manager or MailoutManager()

    def send(self):
        for user in self.manager.users_for_mailout(self.mailout_time):
            self.send_for_user(user)

    def send_for_user(self, user):
        context = {'packages': self.manager.changed_for_user(user)}
        message = render_to_string('watches/emails/changes.txt', context)
        user.email_user(u'Packages changed', message)
        user.watchsettings.last_mailout = self.mailout_time
        user.save()

