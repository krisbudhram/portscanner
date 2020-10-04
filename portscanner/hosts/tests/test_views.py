import pytest
from django.urls import reverse
from nmap import PortScanner
from pytest_django.fixtures import client

from portscanner.hosts import models, views

from .test_helpers import mockNmap


@pytest.mark.django_db
def test_hostscan(client, monkeypatch):
    # Test rendering
    monkeypatch.setattr(PortScanner, "scan", mockNmap().scan)
    monkeypatch.setattr(PortScanner, "all_hosts", mockNmap().all_hosts)
    hostscan_view = reverse("portscanner.hosts:hostscan")
    response = client.get(hostscan_view)

    assert response.status_code == 200

    # Test scan
    response = client.post(hostscan_view, {"target": "192.168.1.1"})

    assert response.status_code == 302
    assert response.url == "/results/192.168.1.1"

    host = models.Host.objects.get(label="192.168.1.1")
    hostscan = models.HostScan.objects.get(target__label="192.168.1.1")

    assert set(["22/tcp", "80/tcp"]) == set(hostscan.ports["open"])


@pytest.mark.django_db
def test_scanresults(client, hostscan):
    # Test rendering
    scanresults_view = reverse("portscanner.hosts:results")
    response = client.get(scanresults_view)

    assert response.status_code == 200
    assert hostscan.target.label in response.content.decode()

    # Test search
    response = client.post(scanresults_view, {"host": hostscan.target.label})

    assert response.status_code == 302
    assert response.url == f"/results/{hostscan.target.label}"


@pytest.mark.django_db
def test_scanresults_host(client, hostscan):
    # Test rendering
    scanresults_view = reverse(
        "portscanner.hosts:results", args=(hostscan.target.label,)
    )
    assert scanresults_view == f"/results/{hostscan.target.label}"

    response = client.get(scanresults_view, {"req_target": "testhost.example.com"})

    assert response.status_code == 200
    assert hostscan.target.label in response.content.decode()

    # Test search
    response = client.post(scanresults_view, {"host": "testhost.example.com"})

    assert response.status_code == 302
    assert response.url == "/results/testhost.example.com"


@pytest.mark.django_db
def test_scanresults_fail(client):
    scanresults_view = reverse("portscanner.hosts:results")
    response = client.post(f"{scanresults_view}/invalid.host")

    assert response.status_code == 404
