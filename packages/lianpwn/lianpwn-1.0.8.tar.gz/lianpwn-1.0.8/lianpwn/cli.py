# cli.py
import click
from lianpwn.template_gen import (
    generate_template,
    generate_template_nocli,
    kernel_upload_template,
)


@click.group()
def cli():
    pass


@cli.command()
def template():
    """Generate a template file"""
    generate_template()


@cli.command()
def nocli():
    """When it comes to burpforce"""
    generate_template_nocli()


@cli.command()
def upload():
    """Upload file to remote"""
    kernel_upload_template()


if __name__ == "__main__":
    cli()
