from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

SLUG_REGEX = '(?P<slug>[a-z0-9-_]+)'


urlpatterns = patterns('main.views',
    # Examples:
    url(r'^$', 'index', name='index'),
    url(r'^about/$', 'about', name='about'),
    url(r'^login/$', 'login_view', name='login'),
    url(r'^logout/$', 'logout_view', name='logout'),
    url(r'^done/$', 'close_modal', name='close_modal'),
)

urlpatterns += patterns('',
    url(r'^instruments/', include('bandbook.instruments.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sentry/', include('sentry.web.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
)
