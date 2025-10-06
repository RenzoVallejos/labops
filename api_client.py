import os
import json
import tempfile

import click
import requests
import urllib3
import difflib
from dotenv import load_dotenv
import time

CACHE_DURATION = 300  # 5 minutes
CACHE_FILE = os.path.join(tempfile.gettempdir(), 'labops_cache.json')

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
API_KEY = os.getenv("API_KEY", "mock-secret-token")




def get_hosts(status=None, platform=None, hostname=None,
              usagetype=None, location=None,
              checkout_owner=None, bmc=False, no_bmc=False, search_all=False):
    """
    Fetch hosts from the API with optional filtering.
    """
    # Check cache first
    now = time.time()
    cache_data = _load_cache()
    
    if 'hosts' in cache_data and now - cache_data.get('hosts_time', 0) < CACHE_DURATION:
        data = cache_data['hosts']
    else:
        # Fetch from API
        click.echo("Fetching hosts from API...")
        headers = {"X-Api-Key": API_KEY}
        response = requests.get(f"{API_BASE_URL}/hosts", headers=headers, verify=False)
        response.raise_for_status()
        data = response.json()
        click.echo(" Data retrieved successfully")

        # Cache the response
        _save_cache('hosts', data, now)

    # Extract hosts array from API response
    if isinstance(data, dict) and 'response' in data:
        hosts = data['response']
    else:
        hosts = data

    # Status filtering
    if status:
        hosts = [h for h in hosts if h.get("status", {}).get("status", "").lower() == status.lower()]
    
    # BMC filtering
    if bmc:
        hosts = [h for h in hosts if h.get("con_ip") and h.get("con_ip").strip()]
    elif no_bmc:
        hosts = [h for h in hosts if not h.get("con_ip") or not h.get("con_ip").strip()]

    # Platform filtering with fuzzy matching
    if platform:
        # Single pass to get platforms and exact matches
        all_platforms = set()
        exact_matches = []

        for h in hosts:
            host_platform = h.get("platform")
            if host_platform:
                all_platforms.add(host_platform)
                if host_platform.lower() == platform.lower():
                    exact_matches.append(h)

        if exact_matches:
            hosts = exact_matches
        else:
            # First try prefix matching (e.g., "monza" matches "MONZA91", "MONZA92", etc.)
            platform_list = list(all_platforms)
            prefix_matches = [p for p in platform_list if p.lower().startswith(platform.lower())]
            
            if prefix_matches:
                close_matches = sorted(prefix_matches)  # Sort alphabetically
            else:
                # Fall back to fuzzy matching if no prefix matches
                platform_list_lower = [p.lower() for p in platform_list]
                close_matches_lower = difflib.get_close_matches(platform.lower(), platform_list_lower, n=10, cutoff=0.2)
                
                # Map back to original case
                close_matches = []
                for match_lower in close_matches_lower:
                    for original in platform_list:
                        if original.lower() == match_lower:
                            close_matches.append(original)
                            break

            if close_matches:
                click.echo(f"No hosts found with platform '{platform}'.\n")
                click.echo("Did you mean one of these?")

                # Pre-calculate counts
                platform_counts = {}
                for h in hosts:
                    p = h.get("platform")
                    if p in close_matches:
                        platform_counts[p] = platform_counts.get(p, 0) + 1

                total_hosts = 0
                for i, match in enumerate(close_matches, 1):
                    count = platform_counts.get(match, 0)
                    total_hosts += count
                    click.echo(f"  {i}. {match} ({count} hosts)")
                
                click.echo(f"\nTotal: {total_hosts} hosts across all {platform.upper()}* platforms")

                choice = click.prompt("\nEnter number to select, or press Enter to cancel",
                                      type=int, default=0, show_default=False)

                if 1 <= choice <= len(close_matches):
                    selected_platform = close_matches[choice - 1]
                    hosts = [h for h in hosts if h.get("platform") == selected_platform]
                    click.echo(f"\nShowing hosts with platform '{selected_platform}'...\n")
                else:
                    return {"response": [], "count": 0}
            else:
                click.echo(f"No hosts found with platform '{platform}' and no similar matches.")
                return {"response": [], "count": 0}

    return {"response": hosts, "count": len(hosts)}




def get_racks(location=None, rack_type=None, lab=None, usage=None, search_all=False):
    now = time.time()
    cache_data = _load_cache()
    
    if 'racks' in cache_data and now - cache_data.get('racks_time', 0) < CACHE_DURATION:
        data = cache_data['racks']
    else:
        click.echo("Fetching racks from API...")
        headers = {"X-Api-Key": API_KEY}
        response = requests.get(f"{API_BASE_URL}/racks", headers=headers, verify=False)
        response.raise_for_status()
        data = response.json()
        click.echo("✓ Data retrieved successfully")
        _save_cache('racks', data, now)

    # Basic local filtering (mock)
    if location:
        data = [r for r in data if r.get("location") == location]

    return data

def get_switches(status=None, rack=None, location=None, search_all=False):
    now = time.time()
    cache_data = _load_cache()
    
    if 'switches' in cache_data and now - cache_data.get('switches_time', 0) < CACHE_DURATION:
        data = cache_data['switches']
    else:
        click.echo("Fetching switches from API...")
        headers = {"X-Api-Key": API_KEY}
        response = requests.get(f"{API_BASE_URL}/switches", headers=headers, verify=False)
        response.raise_for_status()
        data = response.json()
        click.echo("✓ Data retrieved successfully")
        _save_cache('switches', data, now)

    # Basic local filtering (mock)
    if status:
        data = [s for s in data if s.get("status") == status]
    if rack:
        data = [s for s in data if s.get("rack") == rack]

    return data

def get_host_by_asset_id(asset_id):
    """Get host by asset ID"""
    headers = {"X-Api-Key": API_KEY}
    response = requests.get(f"{API_BASE_URL}/hosts/find?assetid={asset_id}", headers=headers, verify=False)
    response.raise_for_status()
    return response.json()

def get_host_by_hardware_id(hardware_id):
    """Get host status by hardware ID"""
    headers = {"X-Api-Key": API_KEY}
    response = requests.get(f"{API_BASE_URL}/hosts/hoststatus?hardwareid={hardware_id}", headers=headers, verify=False)
    response.raise_for_status()
    return response.json()

def _load_cache():
    """Load cache from file"""
    try:
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def _save_cache(key, data, timestamp):
    """Save data to cache file"""
    cache_data = _load_cache()
    cache_data[key] = data
    cache_data[f'{key}_time'] = timestamp
    
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache_data, f)
    except Exception:
        pass  # Fail silently if can't write cache

