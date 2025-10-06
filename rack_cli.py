# Handles CLI interface (Click decorators, options)
import click
from commands.lookup import lookup_host
from commands.list_hosts import list_hosts
from commands.list_racks import list_racks
from commands.list_switches import list_switches
from commands.rack_contents import rack_contents
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
@click.version_option("0.1.0")
@click.pass_context
def cli(ctx):
    """Rack CLI - Manage datacenter host, rack & switch information"""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command(name="hosts")
@click.option('--status', help='Filter hosts by status (Available, Reserved, etc.)')
@click.option('--platform', help='Fuzzy search hosts by platform (case-insensitive)')
@click.option('--hostname', help='Fuzzy search hosts by hostname (case-insensitive)')
@click.option('--usagetype', help='Fuzzy search hosts by usage type (case-insensitive)')
@click.option('--location', help='Fuzzy search hosts by location (case-insensitive)')
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
@click.option('--all', 'search_all', help='Fuzzy search across all fields (case-insensitive)')
def list_hosts_cmd(status, platform, hostname, usagetype, location, checkout_owner, bmc, no_bmc, available, pending, scrapped, reserved, checked_out, in_qual, pre_qual, core_services, liquidated, pending_disposal, returned_vendor, search_all):
    """List all hosts (filter by specific fields or search across all with --all)"""
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
    
    list_hosts(status, platform, hostname, usagetype, location, checkout_owner, bmc, no_bmc, search_all)


@cli.command(name="racks")
def list_racks_cmd():
    """List all racks"""
    list_racks()


@cli.command(name="switches")
def list_switches_cmd():
    """List all switches"""
    list_switches()


@cli.command(name="rack-contents")
@click.option('--rack-id', help='Show all hosts and switches in a rack')
def rack_contents_cmd(rack_id):
    """Show hosts & switches in a given rack"""
    rack_contents(rack_id)


@cli.command(name="summary")
def summary_cmd():
    """Show a summary of datacenter resources"""
    summary()


if __name__ == "__main__":
    cli()
