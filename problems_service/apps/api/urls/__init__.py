from django.urls import include, path

app_name = "api"
api_prefix = "apps.api.urls"

urlpatterns = [
    path("", include(f"{api_prefix}.answers")),
    path("", include(f"{api_prefix}.questions")),
]
