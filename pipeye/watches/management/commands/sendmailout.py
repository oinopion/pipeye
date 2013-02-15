from django.core.management.base import NoArgsCommand
from django.utils import timezone
from ...mailout import Mailout

class Command(NoArgsCommand):
    help = u'Sends mailout to users'

    def handle_noargs(self, **options):
        mailout = Mailout(timezone.now())
        emails_sent = mailout.send()
        self.stdout.write(u'%d emails sent' % emails_sent)

