from django.core.management.base import NoArgsCommand
from ...packages.pypi import Importer

class Command(NoArgsCommand):
    help = 'Synchronizes list of all packages with PyPI'

    def handle(self, **options):
        importer = Importer()
        created = importer.all_packages()
        self.stdout.write('New packages added: %d\n' % created)
