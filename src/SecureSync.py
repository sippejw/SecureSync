import click
import os
import wormhole
import json
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from random_word import RandomWords
from api import WormholeAPI
import time

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
    keystring = str(len(keys))
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
    connection = WormholeAPI()
    while True:
        try:
            connection.receive(keystring)
        except:
            pass

@click.command()
def sync():
    try:
        configfile = open('.SecureSync', 'r')
        config = json.loads(configfile.read())
        configfile.close()
        appid = config['appid']
        relay_url = config['relay_url']
        code = config['key']
    except IOError:
        print('This directory is not linked to a SecureSync instance!')
        return
    connection = WormholeAPI()
    contents = os.listdir(os.getcwd())
    for file in contents:
        if file[0] != '.':
            try:
                res = connection.send(code, os.getcwd() + '/' + file)
            except:
               pass
cli.add_command(init)
cli.add_command(connect)
cli.add_command(sync)


if __name__ == '__main__':
    cli()
