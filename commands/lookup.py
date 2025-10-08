import click
from datetime import datetime
from colorama import Fore, Style, init
from api_client import get_hosts, get_host_by_asset_id, get_host_by_hardware_id, get_k2_ip

init()  # Initialize colorama

def format_host_data(data):
    output = []

    # Key info first
    if data.get('assetid'):
        output.append(f"{Fore.CYAN}Asset ID{Style.RESET_ALL}: {Fore.WHITE}{data['assetid']}{Style.RESET_ALL}")
    if data.get('status', {}).get('status'):
        output.append(f"{Fore.CYAN}Status{Style.RESET_ALL}: {Fore.WHITE}{data['status']['status']}{Style.RESET_ALL}")
    if data.get('location'):
        output.append(f"{Fore.CYAN}Location{Style.RESET_ALL}: {Fore.WHITE}{data['location']}{Style.RESET_ALL}")

    output.append("")  # Spacing

    # Hardware info
    if data.get('platform'):
        output.append(f"{Fore.CYAN}Platform{Style.RESET_ALL}: {Fore.WHITE}{data['platform']}{Style.RESET_ALL}")
    if data.get('manufacturer'):
        output.append(f"{Fore.CYAN}Manufacturer{Style.RESET_ALL}: {Fore.WHITE}{data['manufacturer']}{Style.RESET_ALL}")
    if data.get('hardwareid'):
        output.append(f"{Fore.CYAN}Hardware ID{Style.RESET_ALL}: {Fore.WHITE}{data['hardwareid']}{Style.RESET_ALL}")
    if data.get('hostname'):
        output.append(f"{Fore.CYAN}Hostname{Style.RESET_ALL}: {Fore.WHITE}{data['hostname']}{Style.RESET_ALL}")

    output.append("")  # Spacing

    # Network info
    if data.get('con_ip'):
        output.append(f"{Fore.CYAN}Console IP{Style.RESET_ALL}: {Fore.WHITE}{data['con_ip']}{Style.RESET_ALL}")
    if data.get('lan_ip'):
        output.append(f"{Fore.CYAN}LAN IP{Style.RESET_ALL}: {Fore.WHITE}{data['lan_ip']}{Style.RESET_ALL}")

    # Rack info
    rack = data.get('serverrack', {})
    location = data.get('location', '').strip()
    
    # Show rack info if we have serverrack data or location info
    if rack or location:
        output.append("")
        output.append(f"{Fore.CYAN}Rack Info{Style.RESET_ALL}:")
        
        # Use serverrack data if available, otherwise parse from location
        if rack and rack.get('lab'):
            output.append(f"  {Fore.CYAN}Lab{Style.RESET_ALL}: {Fore.WHITE}{rack['lab']}{Style.RESET_ALL}")
        elif location:
            # Extract lab from location (e.g., SEA85.159.R6-L01 -> SEALAB85)
            if location.startswith('SEA85'):
                output.append(f"  {Fore.CYAN}Lab{Style.RESET_ALL}: {Fore.WHITE}SEALAB85{Style.RESET_ALL}")
        
        if rack and rack.get('position'):
            output.append(f"  {Fore.CYAN}Position{Style.RESET_ALL}: {Fore.WHITE}{rack['position']}{Style.RESET_ALL}")
        elif location:
            # Extract rack position from location
            rack_pos = location.split('.')[0] if '.' in location else location
            if rack_pos:
                output.append(f"  {Fore.CYAN}Position{Style.RESET_ALL}: {Fore.WHITE}{rack_pos}{Style.RESET_ALL}")
        
        if rack and rack.get('consolevlan'):
            vlan = rack['consolevlan']
            if vlan.get('vlanid'):
                output.append(f"  {Fore.CYAN}VLAN ID{Style.RESET_ALL}: {Fore.WHITE}{vlan['vlanid']}{Style.RESET_ALL}")
            if vlan.get('subnet'):
                output.append(f"  {Fore.CYAN}Subnet{Style.RESET_ALL}: {Fore.WHITE}{vlan['subnet']}{Style.RESET_ALL}")

    # Usage info
    if data.get('usagetype', {}).get('usagetype'):
        output.append("")
        output.append(f"{Fore.CYAN}Usage Type{Style.RESET_ALL}: {Fore.WHITE}{data['usagetype']['usagetype']}{Style.RESET_ALL}")
    if data.get('hostclass'):
        output.append(f"{Fore.CYAN}Host Class{Style.RESET_ALL}: {Fore.WHITE}{data['hostclass']}{Style.RESET_ALL}")
    if data.get('installed_os'):
        output.append(f"{Fore.CYAN}OS{Style.RESET_ALL}: {Fore.WHITE}{data['installed_os']}{Style.RESET_ALL}")

    # Timestamp
    if data.get('hwmon_timestamp'):
        try:
            dt = datetime.fromisoformat(data['hwmon_timestamp'].replace('Z', '+00:00'))
            formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
            output.append("")
            output.append(f"{Fore.CYAN}Last Updated{Style.RESET_ALL}: {Fore.WHITE}{formatted_time}{Style.RESET_ALL}")
        except:
            pass

    return "\n".join(output)

def format_host_data_with_k2(data):
    """Format host data with K2 IP lookup for individual host lookups"""
    output = []

    # Key info first
    if data.get('assetid'):
        output.append(f"{Fore.CYAN}Asset ID{Style.RESET_ALL}: {Fore.WHITE}{data['assetid']}{Style.RESET_ALL}")
    if data.get('status', {}).get('status'):
        output.append(f"{Fore.CYAN}Status{Style.RESET_ALL}: {Fore.WHITE}{data['status']['status']}{Style.RESET_ALL}")
    if data.get('location'):
        output.append(f"{Fore.CYAN}Location{Style.RESET_ALL}: {Fore.WHITE}{data['location']}{Style.RESET_ALL}")

    output.append("")  # Spacing

    # Hardware info
    if data.get('platform'):
        output.append(f"{Fore.CYAN}Platform{Style.RESET_ALL}: {Fore.WHITE}{data['platform']}{Style.RESET_ALL}")
    if data.get('manufacturer'):
        output.append(f"{Fore.CYAN}Manufacturer{Style.RESET_ALL}: {Fore.WHITE}{data['manufacturer']}{Style.RESET_ALL}")
    if data.get('hardwareid'):
        output.append(f"{Fore.CYAN}Hardware ID{Style.RESET_ALL}: {Fore.WHITE}{data['hardwareid']}{Style.RESET_ALL}")
    if data.get('hostname'):
        output.append(f"{Fore.CYAN}Hostname{Style.RESET_ALL}: {Fore.WHITE}{data['hostname']}{Style.RESET_ALL}")

    output.append("")  # Spacing

    # Network info - get K2 IP if hardware ID is available
    k2_ip = None
    if data.get('hardwareid'):
        k2_ip = get_k2_ip(data['hardwareid'])
    
    if data.get('con_ip'):
        output.append(f"{Fore.CYAN}Console IP{Style.RESET_ALL}: {Fore.WHITE}{data['con_ip']}{Style.RESET_ALL}")
    if k2_ip:
        output.append(f"{Fore.CYAN}K2 IP{Style.RESET_ALL}: {Fore.WHITE}{k2_ip}{Style.RESET_ALL}")
    if data.get('lan_ip'):
        output.append(f"{Fore.CYAN}LAN IP{Style.RESET_ALL}: {Fore.WHITE}{data['lan_ip']}{Style.RESET_ALL}")

    # Rack info
    rack = data.get('serverrack', {})
    location = data.get('location', '').strip()
    
    # Show rack info if we have serverrack data or location info
    if rack or location:
        output.append("")
        output.append(f"{Fore.CYAN}Rack Info{Style.RESET_ALL}:")
        
        # Use serverrack data if available, otherwise parse from location
        if rack and rack.get('lab'):
            output.append(f"  {Fore.CYAN}Lab{Style.RESET_ALL}: {Fore.WHITE}{rack['lab']}{Style.RESET_ALL}")
        elif location:
            # Extract lab from location (e.g., SEA85.159.R6-L01 -> SEALAB85)
            if location.startswith('SEA85'):
                output.append(f"  {Fore.CYAN}Lab{Style.RESET_ALL}: {Fore.WHITE}SEALAB85{Style.RESET_ALL}")
        
        if rack and rack.get('position'):
            output.append(f"  {Fore.CYAN}Position{Style.RESET_ALL}: {Fore.WHITE}{rack['position']}{Style.RESET_ALL}")
        elif location:
            # Extract rack position from location
            rack_pos = location.split('.')[0] if '.' in location else location
            if rack_pos:
                output.append(f"  {Fore.CYAN}Position{Style.RESET_ALL}: {Fore.WHITE}{rack_pos}{Style.RESET_ALL}")
        
        if rack and rack.get('consolevlan'):
            vlan = rack['consolevlan']
            if vlan.get('vlanid'):
                output.append(f"  {Fore.CYAN}VLAN ID{Style.RESET_ALL}: {Fore.WHITE}{vlan['vlanid']}{Style.RESET_ALL}")
            if vlan.get('subnet'):
                output.append(f"  {Fore.CYAN}Subnet{Style.RESET_ALL}: {Fore.WHITE}{vlan['subnet']}{Style.RESET_ALL}")

    # Usage info
    if data.get('usagetype', {}).get('usagetype'):
        output.append("")
        output.append(f"{Fore.CYAN}Usage Type{Style.RESET_ALL}: {Fore.WHITE}{data['usagetype']['usagetype']}{Style.RESET_ALL}")
    if data.get('hostclass'):
        output.append(f"{Fore.CYAN}Host Class{Style.RESET_ALL}: {Fore.WHITE}{data['hostclass']}{Style.RESET_ALL}")
    if data.get('installed_os'):
        output.append(f"{Fore.CYAN}OS{Style.RESET_ALL}: {Fore.WHITE}{data['installed_os']}{Style.RESET_ALL}")

    # Timestamp
    if data.get('hwmon_timestamp'):
        try:
            dt = datetime.fromisoformat(data['hwmon_timestamp'].replace('Z', '+00:00'))
            formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
            output.append("")
            output.append(f"{Fore.CYAN}Last Updated{Style.RESET_ALL}: {Fore.WHITE}{formatted_time}{Style.RESET_ALL}")
        except:
            pass

    return "\n".join(output)

def lookup_host(asset_id: str = None, hardware_id: str = None):
    """
    Find a host by asset_id or hardware_id and display its details in pretty format.
    """
    if hardware_id:
        try:
            # First get basic info from hardware ID
            hw_result = get_host_by_hardware_id(hardware_id)
            hw_data = hw_result.get('response', hw_result)

            # Extract asset ID and get full details
            if hw_data.get('assetid'):
                full_result = get_host_by_asset_id(hw_data['assetid'])
                display_data = full_result.get('response', full_result)
            else:
                # Fallback to hardware ID data if no asset ID
                display_data = hw_data

            formatted_output = format_host_data_with_k2(display_data)
            click.echo(formatted_output)
        except Exception as e:
            click.echo(f'{{"error": "Hardware ID {hardware_id} not found: {str(e)}"}}')
        return

    try:
        result = get_host_by_asset_id(asset_id)
        display_data = result.get('response', result)
        formatted_output = format_host_data_with_k2(display_data)
        click.echo(formatted_output)
    except Exception as e:
        click.echo(f'{{"error": "Asset ID {asset_id} not found: {str(e)}"}}')
