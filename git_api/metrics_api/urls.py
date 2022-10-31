from django.urls import path
from .views import IssuesMetrics, PersonMetrics

urlpatterns = [
    path("api/issues/", IssuesMetrics.as_view(), name="issue-metrics"),
    path("api/persons/", PersonMetrics.as_view(), name="person-metrics"),
]
