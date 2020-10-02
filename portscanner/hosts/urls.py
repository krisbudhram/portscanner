from django.conf.urls import url

from . import views

app_name = "portscanner.hosts"
urlpatterns = [
    url(r"^$", views.hostscan, name="hostscan"),
    url(r"^results/$", views.ScanResults.as_view(), name="results"),
    url(
        r"^results/(?P<req_target>[\w\.\-]+)$",
        views.ScanResults.as_view(),
        name="results",
    ),
]
