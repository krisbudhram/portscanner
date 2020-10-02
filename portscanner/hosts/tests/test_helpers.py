import pytest
from nmap import PortScanner

from portscanner.hosts.helpers import scan_target, validate_target


class mockNmap:
    def scan(*args, **kwargs):
        return {
            "nmap": {
                "command_line": "nmap -oX - -p 1-1000 -sV testhost.example.com",
                "scaninfo": {"tcp": {"method": "connect", "services": "1-1000"}},
                "scanstats": {
                    "timestr": "Thu Oct  1 20:29:58 2020",
                    "elapsed": "0.35",
                    "uphosts": "1",
                    "downhosts": "0",
                    "totalhosts": "1",
                },
            },
            "scan": {
                "192.168.1.1": {
                    "hostnames": [{"name": "testhost.example.com", "type": "PTR"}],
                    "addresses": {"ipv4": "192.168.1.1"},
                    "vendor": {},
                    "status": {"state": "up", "reason": "conn-refused"},
                    "tcp": {
                        22: {
                            "state": "open",
                            "reason": "syn-ack",
                            "name": "ssh",
                            "product": "OpenSSH",
                            "version": "8.1",
                            "extrainfo": "protocol 2.0",
                            "conf": "10",
                            "cpe": "cpe:/a:openbsd:openssh:8.1",
                        },
                        80: {
                            "state": "open",
                            "reason": "syn-ack",
                            "name": "http",
                            "product": "httpd",
                            "version": "",
                            "extrainfo": "",
                            "conf": "10",
                            "cpe": "cpe:/o:httpd:1.0",
                        },
                    },
                }
            },
        }

    def all_hosts(*args, **kwargs):
        return ["192.168.1.1"]


@pytest.mark.django_db
def test_validate_target(target) -> None:
    assert validate_target(target.label) == False
    target.label = "127.0.0.1"
    assert validate_target(target.label) == True


@pytest.mark.django_db
def test_scan_target(target, monkeypatch) -> None:
    monkeypatch.setattr(PortScanner, "scan", mockNmap().scan)
    monkeypatch.setattr(PortScanner, "all_hosts", mockNmap().all_hosts)
    result = scan_target(target.label)
    assert result["elapsed"] == 1
    assert {"22/tcp", "80/tcp"} == set(result["open_ports"])
