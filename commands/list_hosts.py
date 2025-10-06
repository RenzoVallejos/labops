#  Handles business logic (API calls, formatting)

import click
from datetime import datetime
from colorama import Fore, Style, init
from api_client import get_hosts
from commands.lookup import format_host_data

init()

def format_hosts_list(hosts_data):
    # Extract hosts from response wrapper
    if isinstance(hosts_data, dict) and 'response' in hosts_data:
        hosts = hosts_data['response']
        total_count = hosts_data.get('count', len(hosts))
    else:
        hosts = hosts_data
        total_count = len(hosts)

    output = []
    output.append(f"{Fore.CYAN}Total Hosts: {Fore.WHITE}{total_count}{Style.RESET_ALL}\n")

    for host in hosts:
        if not isinstance(host, dict):
            continue

        # Use the same detailed formatting as format_host_data()
        formatted_host = format_host_data(host)
        output.append(formatted_host)
        output.append("-" * 50)  # Separator between hosts
        output.append("")

    return "\n".join(output)



def list_hosts(status=None, platform=None, hostname=None,
               usagetype=None, location=None,
               checkout_owner=None, bmc=False, no_bmc=False, search_all=False):
    """
    Retrieve and display host information from the API in formatted output.
    """
    hosts = get_hosts(
        status=status,
        platform=platform,
        hostname=hostname,
        usagetype=usagetype,
        location=location,
        checkout_owner=checkout_owner,
        bmc=bmc,
        no_bmc=no_bmc,
        search_all=search_all
    )

    formatted_output = format_hosts_list(hosts)
    click.echo(formatted_output)
