from django.conf.urls.defaults import *
from django.contrib import admin
import settings # Needed for PROJECT_ROOT.

admin.autodiscover()

from coltrane.feeds import CategoryFeed, LatestEntriesFeed

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    #Static media url not needed for production because it is being served by nginx
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    
    (r'^about/', 'django.views.generic.simple.direct_to_template', {'template': 'about.html',
                                                                    'extra_context': {'is_about': True}}),
    (r'^categories/', include('coltrane.urls.categories')),
    (r'^links/', include('coltrane.urls.links')),
    (r'^tags/', include('coltrane.urls.tags')),
    
    (r'^feeds/latest/$', LatestEntriesFeed()),
    # This isn't working yet
    (r'^feeds/categories/(?P<category_name>.*)/$', CategoryFeed()), 
    # This is how we set up the category feed for django 1.2 which used to work ok
    #(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', { 'feed_dict': feeds }),

    (r'', include('coltrane.urls.entries')),
)
