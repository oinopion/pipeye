import hurl

urlpatterns = hurl.patterns('pipeye.watches.views', {
    '': 'watches_list',
    'create': 'create_watch',
})
