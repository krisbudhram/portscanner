import pytest
from nmap import PortScanner

from portscanner.hosts.models import HostScan


@pytest.mark.django_db
def test_hostscan(hostscan, target) -> None:
    hostscan_new = HostScan.objects.create(
        target=target,
        ports={"open": []},
        duration=1,
    )

    result = hostscan_new.changed
    assert "Closed 999/tcp" in result

    hostscan_new2 = HostScan.objects.create(
        target=target,
        ports={"open": ["999/tcp", "22/tcp"]},
        duration=1,
    )
    result = hostscan_new2.changed
    assert "22/tcp" in result
