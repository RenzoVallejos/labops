import click
from colorama import Fore, Style, init
from api_client import get_rack_by_position, get_k2_ip

init()

def format_rack_data(rack):
    """Format a single rack's detailed data for display"""
    output = []
    
    # Key info first
    if rack.get('position'):
        output.append(f"{Fore.CYAN}Rack Position{Style.RESET_ALL}: {Fore.WHITE}{rack['position']}{Style.RESET_ALL}")
    if rack.get('lab'):
        output.append(f"{Fore.CYAN}Lab{Style.RESET_ALL}: {Fore.WHITE}{rack['lab']}{Style.RESET_ALL}")

    
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
        # Sort hosts by location
        hosts = sorted(rack['hosts'], key=lambda x: x.get('location') or '')
        output.append(f"{Fore.CYAN}Hosts in Rack{Style.RESET_ALL}: {Fore.WHITE}{len(hosts)}{Style.RESET_ALL}")
        
        # Table headers
        output.append("")
        header = f"{Fore.CYAN}{'Asset ID':<12} {'Hardware ID':<20} {'Platform':<15} {'BMC IP':<15} {'K2 IP':<15} {'LAN IP':<15}{Style.RESET_ALL}"
        output.append(header)
        output.append("-" * 92)
        
        # Table rows
        for host in hosts:
            if not isinstance(host, dict):
                continue
                
            assetid = (host.get('assetid') or 'N/A')[:11]  # Truncate if too long
            hardwareid = (host.get('hardwareid') or 'N/A')[:19]  # Truncate if too long
            platform = (host.get('platform') or 'N/A')[:14]  # Truncate if too long
            con_ip = (host.get('con_ip') or 'N/A')[:14]  # Truncate if too long
            lan_ip = (host.get('lan_ip') or 'N/A')[:14]  # Truncate if too long
            
            # Get K2 IP if hardware ID is available
            k2_ip = 'N/A'
            if host.get('hardwareid'):
                k2_result = get_k2_ip(host.get('hardwareid'))
                if k2_result:
                    k2_ip = k2_result[:14]  # Truncate if too long
            
            row = f"{Fore.WHITE}{assetid:<12} {hardwareid:<20} {platform:<15} {con_ip:<15} {k2_ip:<15} {lan_ip:<15}{Style.RESET_ALL}"
            output.append(row)
    
    return "\n".join(output)

def lookup_rack(position):
    """Find a rack by position and display its details"""
    try:
        # First try exact match
        rack = get_rack_by_position(position)
        
        # If not found and position has U position (contains dot), try without U position
        if not rack and '.' in position:
            # Extract rack position without U position (e.g., SEA85.159.R6-L10.14 -> SEA85.159.R6-L10)
            rack_only = '.'.join(position.split('.')[:-1])
            rack = get_rack_by_position(rack_only)
        
        if rack:
            formatted_output = format_rack_data(rack)
            click.echo(formatted_output)
        else:
            click.echo(f'{{"error": "Rack position {position} not found"}}')
    except Exception as e:
        click.echo(f'{{"error": "Rack position {position} not found: {str(e)}"}}')