from django.core.management.base import LabelCommand
from ...models import Package
from ...pypi import PackagesImporter

class Command(LabelCommand):
    help = 'Synchronizes one package releases'

    def handle_label(self, label, **options):
        package = Package.objects.get(name=label)
        importer = PackagesImporter()
        releases = importer.sync_package(package)
        self.stdout.write("'%s' releases added: %d\n" % (package, releases))
