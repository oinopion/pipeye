import hurl

urlpatterns = hurl.patterns('pipeye.packages.views', {
    '': 'package_search',
    '<name:str>': 'package_detail',
})
