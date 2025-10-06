import click
import json
from collections import Counter
from api_client import get_hosts, get_racks, get_switches


def summary():
    """
    Show a summary of datacenter resources (JSON format).
    """

    # --- Hosts summary ---
    hosts = get_hosts()
    host_status_counts = Counter(h.get("status") for h in hosts if h.get("status"))

    # --- Racks summary ---
    racks = get_racks()
    total_racks = len(racks)

    # --- Switches summary ---
    switches = get_switches()
    switch_model_counts = Counter(s.get("model") for s in switches if s.get("model"))

    # Build JSON summary
    result = {
        "hosts": {
            "total": len(hosts),
            "by_status": dict(host_status_counts),
        },
        "racks": {
            "total": total_racks,
        },
        "switches": {
            "total": len(switches),
            "by_model": dict(switch_model_counts),
        },
    }

    click.echo(json.dumps(result, indent=4))

