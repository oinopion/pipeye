from datetime import timedelta
from django.core.management.base import NoArgsCommand
from django.utils import timezone
from ...models import PackageImport
from ...pypi import PackagesImporter


class Command(NoArgsCommand):
    help = 'Synchronizes packages using PyPI changelog'

    def handle_noargs(self, **options):
        since = self.since()
        PackageImport.objects.create()
        importer = PackagesImporter()
        result = importer.sync_changed(since)
        msg = "Synced %(new_packages)d packages and %(new_releases)d release"
        self.stdout.write(msg % result)

    def since(self):
        try:
            package_import = PackageImport.objects.latest('timestamp')
            return package_import.timestamp
        except PackageImport.DoesNotExist:
            yesterday = timezone.now() - timedelta(days=1)
            return yesterday
