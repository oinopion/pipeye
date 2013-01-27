import string
from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
from .models import Package, PackageRelease

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


class PackageReleaseAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'package', 'version', 'timestamp')
    ordering = ('timestamp',)
    raw_id_fields = ('package',)
    search_fields = ('package__name', 'version')


admin.site.register(Package, PackageAdmin)
admin.site.register(PackageRelease, PackageReleaseAdmin)

