from django.urls import path
from .webviews import dashboard

urlpatterns = [
    path("", dashboard, name="dashboard"),
]
