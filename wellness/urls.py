from django.urls import path
from . import views

app_name = "wellness"

urlpatterns = [
    path("", views.wellness_index, name="wellness_index"),
    path("calorie_tracker/", views.calorie_tracker, name="calorie_tracker"),
    path("calorie_limits/", views.calorie_limits, name="calorie_limits"),
]
