import click
import json
from api_client import get_switches  # fetches from mock_api via requests


@click.command()
@click.option("--status", default=None, help="Filter switches by status")
@click.option("--rack", default=None, help="Filter switches by rack")
@click.option("--location", default=None, help="(unused in mock API) Filter switches by location")
@click.option("--search-all", is_flag=True, help="Search all switches")
def list_switches_cmd(status, rack, location, search_all):
    """CLI entrypoint for listing switches."""
    list_switches(status, rack, location, search_all)


def list_switches(status=None, rack=None, location=None, search_all=False):
    """
    Retrieve and display switch information from the API in pretty JSON format.
    """

    switches = get_switches(
        status=status,
        rack=rack,
        location=location,
        search_all=search_all,
    )

    if not switches:
        click.echo("[]")  # empty JSON array
        return

    # Print as pretty JSON
    click.echo(json.dumps(switches, indent=4))

