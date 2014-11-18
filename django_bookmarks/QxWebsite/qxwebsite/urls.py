from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
import os

site_media = os.path.dirname(__file__)
site_media = os.path.join(os.path.dirname(site_media), 'finance','site-media')
print site_media
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'QxWebsite.views.home', name='home'),
    # url(r'^QxWebsite/', include('QxWebsite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^site-media/(?P<path>.*)$','django.views.static.serve',{'document_root':site_media}),
    url(r'^finances/$', 'finance.views.get_finance')
)
