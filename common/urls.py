from django.urls import path
from . import views

urlpatterns = [
    path(
        "files/<path:relative_path>/",
        views.protected_media,
        name="protected_media",
    ),
    path("health/", views.health, name="health"),
]
