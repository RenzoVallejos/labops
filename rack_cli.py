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
@click.option('--all', 'search_all', help='Fuzzy search across all fields (case-insensitive)')
def list_hosts_cmd(status, platform, hostname, usagetype, location, checkout_owner, search_all):
    """List all hosts (filter by specific fields or search across all with --all)"""
    list_hosts(status, platform, hostname, usagetype, location, checkout_owner, search_all)


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
