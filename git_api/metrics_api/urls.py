from django.urls import path
from .views import IssuesMetrics

urlpatterns = [
    path("api/", IssuesMetrics.as_view(), name="ts-api"),
]
