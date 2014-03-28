from django.conf.urls import patterns, include, url

from watson import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'atl.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.login, name="login"),
    url(r'^watson/$', views.main, name="main"),
)
