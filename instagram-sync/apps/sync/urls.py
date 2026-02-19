# apps/sync/urls.py
from django.urls import path
from .views import SyncView

app_name = "sync"

urlpatterns = [
    path("sync/", SyncView.as_view(), name="sync"),
]
