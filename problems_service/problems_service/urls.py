from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .doc_urls import urlpatterns as doc_urls


urlpatterns = [
    path('admin/', admin.site.urls),
]

api_urls = [
    path("api/", include("apps.api.urls", namespace='api')),
]


urlpatterns += api_urls


if settings.DEBUG == True:
    urlpatterns += doc_urls