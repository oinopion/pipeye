import hurl

urlpatterns = hurl.patterns('pipeye.watches.views', {
    '': 'watches_list',
    '<package_name:str>/create': 'create_watch',
})
