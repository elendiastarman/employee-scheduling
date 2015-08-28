from django.core.urlresolvers import reverse
from django.conf import settings
from django.conf.urls import patterns, include, url

from manual import views

urlpatterns = patterns('',
    url(r'^$', views.main_view, name='main'),
    url(r'^toc/$', views.main_view, name='main'),
    url(r'^toc/(?P<path>.+)$', views.main_view, name='main'),
##    url(r'^(?P<position>\w+)/$', views.main_view, name='position'),
##    url(r'^(?P<position>\w+)/(?P<group>\w+)/$', views.main_view, name='group'),
##    url(r'^(?P<position>\w+)/(?P<group>\w+)/(?P<page>\w+)$', views.page_view, name='page'),
    url(r'^page/(?P<path>.+)$', views.page_view, name='page'),

)

##if settings.DEBUG:
##    urlpatterns += patterns('',
##        url(r'^(?P<path>.*)$', 'django.views.static.serve', {
##            'document_root': settings.MANUAL_MEDIA,
##        }),
##   )
