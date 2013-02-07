import string
from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
from .models import Package, PackageRelease, PackageImport, PackageReleaseChange

class FirstLetterFilter(SimpleListFilter):
    title = 'first letter'
    parameter_name = 'first_letter'

    def lookups(self, request, model_admin):
        return zip(string.ascii_uppercase, string.ascii_uppercase)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(name__istartswith=self.value())


class PackageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = (FirstLetterFilter,)
    ordering = ('name',)
    search_fields = ('name',)
    raw_id_fields = ('latest_release',)


class PackageReleaseAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'package', 'version', 'timestamp')
    ordering = ('timestamp',)
    raw_id_fields = ('package',)
    search_fields = ('package__name', 'version')


class PackageReleaseChangeAdmin(admin.ModelAdmin):
    list_display = ('package', 'release', 'timestamp')
    search_fields = ('package__name', 'release__version')
    date_hierarchy = 'timestamp'
    raw_id_fields = ('package', 'release')


class PackageImportAdmin(admin.ModelAdmin):
    list_display = ('timestamp',)
    date_hierarchy = 'timestamp'


admin.site.register(Package, PackageAdmin)
admin.site.register(PackageRelease, PackageReleaseAdmin)
admin.site.register(PackageReleaseChange, PackageReleaseChangeAdmin)
admin.site.register(PackageImport, PackageImportAdmin)
