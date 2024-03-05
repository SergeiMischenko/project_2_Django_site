from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from funnytail.views import page_not_found
from testdjangosite import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("funnytail.urls")),
    path("users/", include("users.urls", namespace="users")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("social-auth/", include("social_django.urls", namespace="social")),
    path("captcha/", include("captcha.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Породы кошек и их описание"
