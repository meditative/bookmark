from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
import os
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

site_media = os.path.dirname(__file__)
site_media = os.path.join(os.path.dirname(site_media), 'bookmarks','site_media')

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_bookmarks.views.home', name='home'),
    # url(r'^django_bookmarks/', include('django_bookmarks.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	url(r'^$','bookmarks.views.main_page'),
	url(r'^user/(\w+)/$','bookmarks.views.user_page'),
	url(r'^login/$','django.contrib.auth.views.login'),
	url(r'^logout/$','bookmarks.views.logout_page'),
	url(r'^site_media/(?P<path>.*)$','django.views.static.serve',{'document_root':site_media}),
	url(r'^register/$','bookmarks.views.register_page'),
	url(r'^register/success/$', direct_to_template,{ 'template': 'registration/register_success.html' }),
	url(r'^save/$','bookmarks.views.bookmark_save_page'),
	url(r'^tag/([^\s]+)/$', 'bookmarks.views.tag_page'),
	url(r'^tag/$', 'bookmarks.views.tag_cloud_page'),
	url(r'^search/$', 'bookmarks.views.search_page'),
	url(r'^ajax/tag/autocomplete/$', 'bookmarks.views.ajax_tag_autocomplete'),
	url(r'^vote/$', 'bookmarks.views.bookmark_vote_page'),
	url(r'^popular/', 'bookmarks.views.popular_page'),
	url(r'^comments/', 'django.contrib.comments.urls.comments'),
	url(r'^bookmark/(\d+)/$', 'bookmarks.views.bookmark_page'),
)
