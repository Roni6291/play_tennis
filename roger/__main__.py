import click

from .cli import run_inference


@click.group()
def main():
    """Welcome to `Roger`"""
    ...


main.add_command(run_inference)

if __name__ == '__main__':
    main()
