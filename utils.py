from rich.console import Console
from rich.table import Table

console = Console()

def print_table(data, fields):
    """
    Pretty-print a list of dictionaries using rich.

    :param data: List of dicts (from CSV or elsewhere)
    :param fields: List of keys to display as columns
    """
    table = Table(show_header=True, header_style="bold magenta")
    
    for field in fields:
        table.add_column(field, style="cyan")

    for row in data:
        table.add_row(*(str(row.get(f, "")) for f in fields))

    console.print(table)

