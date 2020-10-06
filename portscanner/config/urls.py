from django.conf.urls import include, url
from django.contrib.staticfiles import views

urlpatterns = [
    url(r"", include("portscanner.hosts.urls")),
    url(r"^static/(?P<path>.*)$", views.serve),
]
