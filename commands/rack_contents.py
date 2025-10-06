import click
import json
from api_client import get_racks, get_hosts, get_switches


def rack_contents(rack_id: str):
    """
    Show all hosts and switches in a given rack (JSON format).
    """
    if not rack_id:
        click.echo('{"error": "Please provide a rack ID using --rack-id"}')
        return

    # Fetch rack info
    racks = get_racks()
    rack = next((r for r in racks if r.get("rack_id") == rack_id), None)

    if not rack:
        click.echo(f'{{"warning": "Rack {rack_id} not found"}}')
        return

    # Fetch hosts & switches
    hosts = get_hosts()
    rack_hosts = [h for h in hosts if h.get("rack") == rack_id]

    switches = get_switches()
    rack_switches = [s for s in switches if s.get("rack") == rack_id]

    # Build combined result
    result = {
        "rack": rack,
        "hosts": rack_hosts,
        "switches": rack_switches,
    }

    # Output JSON
    click.echo(json.dumps(result, indent=4))

