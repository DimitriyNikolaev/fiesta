from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout_then_login
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from fiesta_core.app import application
from fiesta import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fiesta.views.home', name='home'),
    # url(r'^fiesta/', include('fiesta.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'', include(application.urls)),
    url(r'^login$', login, { "template_name": "partials/auth_tag.html" }, name='login' ),
    url(r'^logout$', logout_then_login, name='logout' )
)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)