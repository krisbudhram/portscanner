"""
Testing fixtures
"""
import pytest

from portscanner.hosts.models import Host, HostScan


@pytest.fixture()
def hostscan(target):
    return HostScan.objects.create(
        target=target, ports={"open": ["999/tcp"]}, duration=20
    )


@pytest.fixture()
def target():
    return Host.objects.create(label="testhost.example.com")
