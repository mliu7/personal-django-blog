from django.conf.urls.defaults import *
from django.contrib import admin
import settings # Needed for PROJECT_ROOT.
admin.autodiscover()

from coltrane.feeds import CategoryFeed, LatestEntriesFeed

feeds = { 'entries': LatestEntriesFeed,
          'categories': CategoryFeed }

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    
    (r'^categories/', include('coltrane.urls.categories')),
    (r'^links/', include('coltrane.urls.links')),
    (r'^tags/', include('coltrane.urls.tags')),
    
    #(r'^weblog/feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', { 'feed_dict': feeds }),

    (r'', include('coltrane.urls.entries')),
                        
    (r'', include('django.contrib.flatpages.urls')),
)