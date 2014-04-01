from django.conf.urls import patterns, include, url

from watson import views
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'atl2.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', views.login, name="login"),
                       url(r'^watson(?:/)?(?P<session>[\s\w]+)?(?:/)?(?P<number>[\s\w]+)?$', views.main, name="main"),
                       url(r'^sessions/$', views.sessions, name="sessions"),
                       url(r'^next/$', views.next, name="next"),
)
