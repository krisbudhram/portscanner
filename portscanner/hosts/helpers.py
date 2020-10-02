import math
from socket import gaierror, gethostbyname

import nmap

PORT_RANGE = "1-1000"


def validate_target(target: str) -> bool:
    """
    Validates that the user-supplied target string is a resolvable
    hostname or IP address.
    """
    try:
        gethostbyname(target)
    except gaierror:
        return False
    return True


def scan_target(target: str) -> dict:
    """
    Nmap scans the target and returns a list of open ports and scan time (in seconds)
    """
    results = {}
    nm = nmap.PortScanner()
    scan = nm.scan(target, PORT_RANGE)
    try:
        results["elapsed"] = math.ceil(float(scan["nmap"]["scanstats"]["elapsed"]))
    except KeyError:
        return {}

    try:
        try:
            scan_host = nm.all_hosts()[0]
        except IndexError:
            return {}
        host_info = scan["scan"][scan_host]
        results["open_ports"] = []
        # TODO: Fix monkeypatch and replace with nm[scan_host].all_protocols()
        for proto in ["tcp", "udp"]:
            # Ensure only open ports are tracked.
            results["open_ports"].extend(
                [
                    f"{port}/{proto}"
                    for port in host_info[proto]
                    if host_info[proto][port]["state"] == "open"
                ]
            )
    except KeyError:
        pass

    return results
