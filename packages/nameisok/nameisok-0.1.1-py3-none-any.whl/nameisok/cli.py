import click

from .core import get_status_package_cli


@click.command()
@click.argument("name")
def main(name):
    """CLI command to check PyPI package name availability."""
    get_status_package_cli(name)
    print('\n')


if __name__ == "__main__":
    main()
