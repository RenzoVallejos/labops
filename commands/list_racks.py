import click
import json
from api_client import get_racks  # fetches from mock_api via requests


@click.command()
@click.option("--location", default=None, help="Filter racks by location")
@click.option("--type", "rack_type", default=None, help="Filter racks by type")
@click.option("--lab", default=None, help="Filter racks by lab (unused in mock API)")
@click.option("--usage", default=None, help="Filter racks by usage (unused in mock API)")
@click.option("--search-all", is_flag=True, help="Search all racks")
def list_racks_cmd(location, rack_type, lab, usage, search_all):
    """CLI entrypoint for listing racks."""
    list_racks(location, rack_type, lab, usage, search_all)


def list_racks(location=None, rack_type=None, lab=None, usage=None, search_all=False):
    """
    Retrieve and display rack information from the API in pretty JSON format.
    """

    racks = get_racks(
        location=location,
        rack_type=rack_type,
        lab=lab,
        usage=usage,
        search_all=search_all,
    )

    if not racks:
        click.echo("[]")  # empty JSON array
        return

    # Print as pretty JSON
    click.echo(json.dumps(racks, indent=4))

