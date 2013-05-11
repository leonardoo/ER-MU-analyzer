from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^', include('data_MU.urls')),
    # Examples:
    # url(r'^$', 'analizer_MU.views.home', name='home'),
    # url(r'^analizer_MU/', include('analizer_MU.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
	 urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)