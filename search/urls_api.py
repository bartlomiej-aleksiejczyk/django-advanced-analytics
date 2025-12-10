from django.urls import path

from . import views

app_name = "search_api"

urlpatterns = [
    path("global/", views.global_search_api, name="global_search_ajax"),
]
