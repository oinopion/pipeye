from django.core.management.base import NoArgsCommand
from ...pypi import PackagesImporter

class Command(NoArgsCommand):
    help = 'Synchronizes list of all packages with PyPI'

    def handle_noargs(self, **options):
        importer = PackagesImporter()
        created = importer.all_packages()
        self.stdout.write('New packages added: %d\n' % created)
