import click
import os


@click.group()
def cli():
    pass


@click.command()
def init():
    click.echo("Initializing")
    if os.path.isfile('.SecureSync'):
        click.echo('This directory is already linked to a SecureSync instance!')
        return


@click.command()
def connect():
    click.echo("Connecting!")
    if os.path.isfile('.SecureSync'):
        click.echo('This directory is already linked to a SecureSync instance!')
        return


@click.command()
def sync():
    click.echo("Syncing!")
    try:
        f = open('.SecureSync')
        f.close()
    except IOError:
        print('This directory is not linked to a SecureSync instance!')
        return


cli.add_command(init)
cli.add_command(connect)
cli.add_command(sync)

if __name__ == '__main__':
    cli()
