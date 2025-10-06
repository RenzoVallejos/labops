import click
from datetime import datetime
from colorama import Fore, Style, init
from api_client import get_hosts

init()

def format_hosts_list(hosts_data):
    if not hosts_data:
        return "No hosts found."

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

        output.append(f"{Fore.CYAN}Asset ID{Style.RESET_ALL}: {Fore.WHITE}{host.get('assetid', 'N/A')}{Style.RESET_ALL}")

        if host.get('status', {}).get('status'):
            status = host['status']['status']
            output.append(f"  {Fore.CYAN}Status{Style.RESET_ALL}: {Fore.WHITE}{status}{Style.RESET_ALL}")

        if host.get('platform'):
            output.append(f"  {Fore.CYAN}Platform{Style.RESET_ALL}: {Fore.WHITE}{host['platform']}{Style.RESET_ALL}")

        if host.get('location') and host['location'] != 'not set':
            output.append(f"  {Fore.CYAN}Location{Style.RESET_ALL}: {Fore.WHITE}{host['location']}{Style.RESET_ALL}")
        elif host.get('serverrack', {}).get('position'):
            output.append(f"  {Fore.CYAN}Location{Style.RESET_ALL}: {Fore.WHITE}{host['serverrack']['position']}{Style.RESET_ALL}")

        if host.get('hardwareid'):
            output.append(f"  {Fore.CYAN}Hardware ID{Style.RESET_ALL}: {Fore.WHITE}{host['hardwareid']}{Style.RESET_ALL}")

        output.append("")  # Spacing between hosts

    return "\n".join(output)



@click.command()
@click.option("--status", default=None, help="Filter hosts by status")
@click.option("--platform", default=None, help="Filter hosts by platform")
@click.option("--hostname", default=None, help="Filter hosts by hostname")
@click.option("--usagetype", default=None, help="Filter hosts by usage type")
@click.option("--location", default=None, help="Filter hosts by location")
@click.option("--checkout-owner", default=None, help="Filter hosts by checkout owner")
@click.option("--search-all", is_flag=True, help="Search all hosts")
def list_hosts_cmd(status, platform, hostname, usagetype, location, checkout_owner, search_all):
    """CLI entrypoint for listing hosts."""
    list_hosts(status, platform, hostname, usagetype, location, checkout_owner, search_all)

def list_hosts(status=None, platform=None, hostname=None,
               usagetype=None, location=None,
               checkout_owner=None, search_all=False):
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
        search_all=search_all
    )

    formatted_output = format_hosts_list(hosts)
    click.echo(formatted_output)
