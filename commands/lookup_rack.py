import click
from colorama import Fore, Style, init
from api_client import get_rack_by_position

init()

def format_rack_data(rack):
    """Format a single rack's detailed data for display"""
    output = []
    
    # Key info first
    if rack.get('position'):
        output.append(f"{Fore.CYAN}Rack Position{Style.RESET_ALL}: {Fore.WHITE}{rack['position']}{Style.RESET_ALL}")
    if rack.get('lab'):
        output.append(f"{Fore.CYAN}Lab{Style.RESET_ALL}: {Fore.WHITE}{rack['lab']}{Style.RESET_ALL}")
    if rack.get('host_count'):
        output.append(f"{Fore.CYAN}Host Count{Style.RESET_ALL}: {Fore.WHITE}{rack['host_count']}{Style.RESET_ALL}")
    
    # Console VLAN info
    if rack.get('consolevlan'):
        vlan = rack['consolevlan']
        if vlan.get('vlanid') or vlan.get('subnet'):
            output.append("")
            output.append(f"{Fore.CYAN}Console VLAN{Style.RESET_ALL}:")
            if vlan.get('vlanid'):
                output.append(f"  {Fore.CYAN}VLAN ID{Style.RESET_ALL}: {Fore.WHITE}{vlan['vlanid']}{Style.RESET_ALL}")
            if vlan.get('subnet'):
                output.append(f"  {Fore.CYAN}Subnet{Style.RESET_ALL}: {Fore.WHITE}{vlan['subnet']}{Style.RESET_ALL}")
    
    # Hosts in rack
    if rack.get('hosts'):
        output.append("")
        output.append(f"{Fore.CYAN}Hosts in Rack{Style.RESET_ALL}:")
        
        # Sort hosts by location
        hosts = sorted(rack['hosts'], key=lambda x: x.get('location') or '')
        
        for host in hosts:
            location = host.get('location', 'N/A')
            host_line = f"  {Fore.CYAN}{location}{Style.RESET_ALL}: "
            host_line += f"{Fore.WHITE}{host.get('assetid', 'N/A')}{Style.RESET_ALL} "
            host_line += f"({host.get('platform', 'Unknown')}) "
            host_line += f"- {host.get('status', 'Unknown')}"
            output.append(host_line)
    
    return "\n".join(output)

def lookup_rack(position):
    """Find a rack by position and display its details"""
    try:
        rack = get_rack_by_position(position)
        if rack:
            formatted_output = format_rack_data(rack)
            click.echo(formatted_output)
        else:
            click.echo(f'{{"error": "Rack position {position} not found"}}')
    except Exception as e:
        click.echo(f'{{"error": "Rack position {position} not found: {str(e)}"}}')