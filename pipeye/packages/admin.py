from django.contrib import admin
from .models import Package, PackageRelease


class PackageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)


class PackageReleaseAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'package', 'version', 'timestamp')
    ordering = ('timestamp', )


admin.site.register(Package, PackageAdmin)
admin.site.register(PackageRelease, PackageReleaseAdmin)

