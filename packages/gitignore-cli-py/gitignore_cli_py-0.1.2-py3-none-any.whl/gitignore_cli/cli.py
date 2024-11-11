import click
from gitignore_cli.generator import generate_gitignore
from gitignore_cli.utils import list_available_templates
import shutil

# Create a command group
@click.group()
def cli():
    """CLI tool to generate .gitignore files from templates."""
    pass

# Autocomplete function for the templates
def template_autocomplete(ctx, param, incomplete):
    available_templates = list_available_templates()
    return [template for template in available_templates if template.startswith(incomplete)]

# Function to display templates in multiple columns
def display_in_columns(data, column_width=20):
    """Displays data in multiple columns based on terminal size."""
    # Get terminal size
    terminal_size = shutil.get_terminal_size((80, 20))
    columns = max(1, terminal_size.columns // column_width)

    # Break the templates into rows and columns
    for i in range(0, len(data), columns):
        row = data[i:i + columns]
        # Join the row with proper spacing
        print("".join(template.ljust(column_width) for template in row))

# Command to generate the .gitignore file
@cli.command()
@click.argument('template_names', nargs=-1, required=True, shell_complete=template_autocomplete)
@click.option('--output', default='.gitignore', help='Output file name')
@click.option('--no-header', is_flag=True, help='Disable the custom header in the generated file')
def generate(template_names, output, no_header):
    """Generates a .gitignore file by combining multiple templates."""
    try:
        generate_gitignore(template_names, output, no_header)
        click.echo(f'.gitignore successfully generated: {output}')
    except FileNotFoundError as e:
        click.echo(f'Error: {e}')

# Command to list all available templates in multiple columns
@cli.command()
def list_templates():
    """Lists all available templates."""
    templates = list_available_templates()
    click.echo("Available templates:\n")
    display_in_columns(templates)

if __name__ == '__main__':
    cli()
