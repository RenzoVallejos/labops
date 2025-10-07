#  Handles business logic (API calls, formatting)

import click
from datetime import datetime
from colorama import Fore, Style, init
from api_client import get_hosts
from commands.lookup import format_host_data

init()

#Display and presentation (UI logic)
def format_hosts_list(hosts_data):
    # Extract hosts from response wrapper
    if isinstance(hosts_data, dict) and 'response' in hosts_data:
        hosts = hosts_data['response']
        shown_count = hosts_data.get('count', len(hosts))
        total_available = hosts_data.get('total_available', shown_count)
    else:
        hosts = hosts_data
        shown_count = len(hosts)
        total_available = shown_count

    output = []

    for host in hosts:
        if not isinstance(host, dict):
            continue

        # Use the same detailed formatting as format_host_data()
        formatted_host = format_host_data(host)
        output.append(formatted_host)
        output.append("-" * 50)  # Separator between hosts
        output.append("")

    # Add count at the bottom
    if shown_count < total_available:
        output.append(f"{Fore.CYAN}Showing: {Fore.WHITE}{shown_count}{Fore.CYAN} of {Fore.WHITE}{total_available}{Fore.CYAN} total hosts{Style.RESET_ALL}")
    else:
        output.append(f"{Fore.CYAN}Total Hosts: {Fore.WHITE}{shown_count}{Style.RESET_ALL}")

    return "\n".join(output)



def list_hosts(status=None, platform=None, hostname=None,
               usagetype=None, location=None,
               checkout_owner=None, bmc=False, no_bmc=False, limit=None, search_all=False):
    """
    Retrieve and display host information from the API in formatted output.72
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
        limit=limit,
        search_all=search_all
    )

    formatted_output = format_hosts_list(hosts)
    click.echo(formatted_output)
