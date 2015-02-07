from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'aabenthus_com.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^authorize$', 'aabenthus_com.google.views.authorize', name='authorize'),
    url(r'^oauth2callback$', 'aabenthus_com.google.views.oauth2callback', name='oauth2callback'),
)
