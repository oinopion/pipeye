from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'pipeye.views.home', name='home'),

    # github login
    url(r'^login/$', 'social_auth.views.auth',
            {'backend': 'github'}, name='login'),
    url(r'^login/complete/(?P<backend>\w+)/$',
            'social_auth.views.complete', name='login_complete'),
)
