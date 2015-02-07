from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'aabenthus_com.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^google/', include('aabenthus_com.google.urls')),
    url(r'^rooms/', include('aabenthus_com.rooms.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
