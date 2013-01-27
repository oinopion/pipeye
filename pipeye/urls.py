from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'pipeye.views.home', name='home'),

    # github login
    url(r'^login/$', 'social_auth.views.auth',
            {'backend': 'github'}, name='login'),
    url(r'^login/complete/(?P<backend>\w+)/$',
            'social_auth.views.complete', name='login_complete'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
            {'next_page': reverse_lazy('home')}, name='logout'),

    # admin
    url(r'^admin/', include(admin.site.urls)),
)
