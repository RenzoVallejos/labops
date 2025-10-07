import click
from colorama import Fore, Style, init
from api_client import get_racks

init()

def format_rack_data(rack):
    """Format a single rack's data for display"""
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
    
    # Host summary by status
    if rack.get('hosts'):
        output.append("")
        output.append(f"{Fore.CYAN}Hosts by Status{Style.RESET_ALL}:")
        
        status_counts = {}
        for host in rack['hosts']:
            status = host.get('status', 'Unknown')
            status_counts[status] = status_counts.get(status, 0) + 1
        
        for status, count in sorted(status_counts.items()):
            output.append(f"  {Fore.CYAN}{status}{Style.RESET_ALL}: {Fore.WHITE}{count}{Style.RESET_ALL}")
    
    return "\n".join(output)

def format_racks_list(racks_data):
    """Format the list of racks for display"""
    output = []
    
    for rack in racks_data:
        if not isinstance(rack, dict):
            continue
        
        formatted_rack = format_rack_data(rack)
        output.append(formatted_rack)
        output.append("-" * 50)  # Separator between racks
        output.append("")
    
    # Add count at the bottom
    total_count = len(racks_data)
    output.append(f"{Fore.CYAN}Total Racks: {Fore.WHITE}{total_count}{Style.RESET_ALL}")
    
    return "\n".join(output)

def list_racks(position=None, limit=None):
    """
    Retrieve and display rack information from the API in formatted output.
    """
    racks = get_racks()
    
    if position:
        racks = [r for r in racks if r.get('position') == position]
    
    # Sort by position for consistent output
    racks.sort(key=lambda x: x.get('position', ''))
    
    # Apply limit if specified
    total_count = len(racks)
    if limit and limit > 0:
        racks = racks[:limit]
    
    formatted_output = format_racks_list(racks)
    click.echo(formatted_output)

