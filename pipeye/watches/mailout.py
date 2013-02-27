from django.core.mail.message import EmailMessage
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
        users = self.manager.users_for_mailout(self.mailout_time)
        for user in users:
            self.send_for_user(user)
        return len(users)

    def send_for_user(self, user):
        email = self.email_for_user(user)
        email.send()
        user.last_mailout = self.mailout_time
        user.save()
        
    def email_for_user(self, user):
        context = {'packages': self.manager.changed_for_user(user)}
        body = render_to_string('watches/emails/changes.txt', context)
        email = EmailMessage(u'Packages changed', body, to=[user.email])
        return email

