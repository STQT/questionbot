from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView, \
    SpectacularJSONAPIView
from django.views.generic import RedirectView
from django.views import defaults as default_views

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('', RedirectView.as_view(url=settings.ADMIN_URL, permanent=True)),
    path("v1/", include("api.core.api_router"), name="v1"),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='api-schema'), name='redoc'),
    path('api/schema/json/', SpectacularJSONAPIView.as_view(), name='json'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
admin.site.site_title = "Boshqaruv paneli"
admin.site.site_header = "Boshqaruv paneli"
admin.site.site_url = "https://t.me/" + settings.TELEGRAM_USERNAME
admin.site.index_title = "Question"
