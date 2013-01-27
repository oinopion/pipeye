from django.contrib import admin
from pipeye.watches.models import Watch


class WatchAdmin(admin.ModelAdmin):
    list_display = ('pk', '__unicode__', 'user', 'package', 'created')
    list_display_links = ('pk', '__unicode__')
    date_hierarchy = 'created'
    raw_id_fields = ('user', 'package')
    ordering = ('-created', )


admin.site.register(Watch, WatchAdmin)
