# Handles CLI interface (Click decorators, options)
import click
from commands.lookup import lookup_host
from commands.lookup_rack import lookup_rack
from commands.list_hosts import list_hosts
from commands.list_racks import list_racks
from commands.list_switches import list_switches
from commands.summary import summary


class CustomGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        # First try to get a regular command from registered commands
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv

        # If no command found, treat as host ID lookup
        def host_lookup_command(host_id=cmd_name):
            if '.' in host_id or any(c.isalpha() for c in host_id):
                lookup_host(None, host_id)
            else:
                lookup_host(host_id, None)

        # Create a dynamic command
        return click.Command(cmd_name, callback=host_lookup_command)


@click.group(cls=CustomGroup, invoke_without_command=True)
@click.version_option("1.0.0")
@click.pass_context
def cli(ctx):
    """LabOps - Datacenter Lab Resource Management CLI
    
    A powerful command-line tool for managing and discovering datacenter lab resources.
    Quickly find hosts, explore rack contents, and navigate inventory with advanced
    filtering and search capabilities.
    
    \b
    Examples:
      labops 1234567890                    # Lookup host by asset ID
      labops hosts --available --limit 10  # List 10 available hosts
      labops hosts --platform dell         # Find DELL hosts with fuzzy matching
      labops hosts --location all          # Search all datacenters globally
      labops rack R1-A01                   # Show detailed rack contents
      labops racks --limit 20              # List first 20 racks
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command(name="hosts")
@click.option('--status', help='Filter hosts by status (Available, Reserved, etc.)')
@click.option('--platform', help='Fuzzy search hosts by platform (case-insensitive)')
@click.option('--hostname', help='Fuzzy search hosts by hostname (case-insensitive)')
@click.option('--usagetype', help='Fuzzy search hosts by usage type (case-insensitive)')
@click.option('--location', help='Filter by location prefix (e.g., sea85, sjc) or use "all" for all locations')
@click.option('--checkout-owner', help='Fuzzy search hosts by checkout owner (case-insensitive)')
@click.option('--bmc', is_flag=True, help='Show only hosts with console IP addresses')
@click.option('--no-bmc', is_flag=True, help='Show only hosts without console IP addresses')
@click.option('--available', is_flag=True, help='Show only available hosts')
@click.option('--pending', is_flag=True, help='Show only hosts pending admin')
@click.option('--scrapped', is_flag=True, help='Show only scrapped hosts')
@click.option('--reserved', is_flag=True, help='Show only reserved hosts')
@click.option('--checked-out', is_flag=True, help='Show only checked out hosts')
@click.option('--in-qual', is_flag=True, help='Show only hosts in qual')
@click.option('--pre-qual', is_flag=True, help='Show only hosts in pre-qual')
@click.option('--core-services', is_flag=True, help='Show only core services hosts')
@click.option('--liquidated', is_flag=True, help='Show only liquidated hosts')
@click.option('--pending-disposal', is_flag=True, help='Show only hosts pending disposal')
@click.option('--returned-vendor', is_flag=True, help='Show only hosts returned to vendor')
@click.option('--limit', type=int, help='Limit number of results (e.g., --limit 50)')
@click.option('--all', 'search_all', help='Fuzzy search across all fields (case-insensitive)')
def list_hosts_cmd(status, platform, hostname, usagetype, location, checkout_owner, bmc, no_bmc, available, pending, scrapped, reserved, checked_out, in_qual, pre_qual, core_services, liquidated, pending_disposal, returned_vendor, limit, search_all):
    """List and filter datacenter hosts with advanced search capabilities
    
    Defaults to SEA85 location for performance. Use --location all for global search.
    Supports fuzzy matching on platforms and multiple filtering options.
    """
    # Convert flag shortcuts to status filter
    if available:
        status = 'Available'
    elif pending:
        status = 'Pending Admin'
    elif scrapped:
        status = 'Scrapped'
    elif reserved:
        status = 'Reserved'
    elif checked_out:
        status = 'Checked Out'
    elif in_qual:
        status = 'In Qual'
    elif pre_qual:
        status = 'Pre-Qual'
    elif core_services:
        status = 'Core Services'
    elif liquidated:
        status = 'Liquidated'
    elif pending_disposal:
        status = 'Pending Disposal'
    elif returned_vendor:
        status = 'Returned to Vendor'
    
    list_hosts(status, platform, hostname, usagetype, location, checkout_owner, bmc, no_bmc, limit, search_all)


@cli.command(name="racks")
@click.option('--position', help='Filter by specific rack position')
@click.option('--limit', type=int, help='Limit number of results')
def list_racks_cmd(position, limit):
    """List datacenter racks with host counts and status summaries
    
    Shows rack positions, host counts, and status breakdowns.
    Filter by specific rack position or limit results.
    """
    list_racks(position=position, limit=limit)


@cli.command(name="switches")
def list_switches_cmd():
    """List network switches and infrastructure devices
    
    Display switch inventory and network infrastructure information.
    """
    list_switches()


@cli.command(name="rack")
@click.argument('position')
def rack_cmd(position):
    """Show detailed rack contents including all hosts and their specifications
    
    Displays a comprehensive table with asset IDs, hardware IDs, platforms,
    BMC IPs, and LAN IPs for all hosts in the specified rack.
    """
    lookup_rack(position)


@cli.command(name="summary")
def summary_cmd():
    """Display datacenter resource summary and health overview
    
    Provides high-level statistics on host counts, rack utilization,
    and overall datacenter capacity and status.
    """
    summary()


if __name__ == "__main__":
    cli()
