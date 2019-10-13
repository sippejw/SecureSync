import click
import os
import wormhole
import json
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from random_word import RandomWords


@click.group()
def cli():
    pass


@click.command()
def init():
    if os.path.isfile('.SecureSync'):
        click.echo('This directory is already linked to a SecureSync instance!')
        return
    generator = RandomWords()
    keys = generator.get_random_words(maxLength=5)
    keystring = "secure"
    for key in keys:
        keystring += "-" + key

    config = {
        "appid": "https://github.com/sippejw/SecureSync",
        "relay_url": "ws://relay.magic-wormhole.io:4000/v1",
        "key": keystring
    }
    configfile = open(".SecureSync", "w+")
    configfile.write(json.dumps(config))
    click.echo("Successfully initialized!")
    click.echo("When connecting use the following key: " + keystring)


@click.command()
def connect():
    if os.path.isfile('.SecureSync'):
        click.echo('This directory is already linked to a SecureSync instance!')
        return
    keystring = input('Please input key given by init: ')
    config = {
        "appid": "https://github.com/sippejw/SecureSync",
        "relay_url": "ws://relay.magic-wormhole.io:4000/v1",
        "key": keystring
    }
    configfile = open(".SecureSync", "w+")
    configfile.write(json.dumps(config))
    configfile.close()
    click.echo("Connected!")


@click.command()
@inlineCallbacks
def sync():
    click.echo("Syncing!")
    try:
        configfile = open('.SecureSync', 'r')
        config = json.loads(configfile.read())
        configfile.close()
        appid = config['appid']
        relay_url = config['relay_url']
    except IOError:
        print('This directory is not linked to a SecureSync instance!')
        return
    connection = wormhole.create("https://github.com/sippejw/SecureSync", "ws://relay.magic-wormhole.io:4000/v1", reactor)
    connection.allocate_code()
    code = yield connection.get_code()
    print("code:", code)
    connection.send_message(b"outbound data")
    inbound = yield connection.get_message()
    yield connection.close()


cli.add_command(init)
cli.add_command(connect)
cli.add_command(sync)


if __name__ == '__main__':
    cli()
