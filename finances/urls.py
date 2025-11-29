from django.urls import path
from . import views

app_name = "finance"

urlpatterns = [
    path("transactions/", views.transaction_list, name="transaction_list"),
]
