from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from scoreboard import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gamesite.views.home', name='home'),
     url(r'^$', 'scoreboard.views.index', name='homepage'),
     url(r'^login/$', 'scoreboard.views.login', name='login'),
     url(r'^logout/$', 'scoreboard.views.logout', name='logout'),
     url(r'^scoreboard/$', 'scoreboard.views.scoreboard', name='scoreboard'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
