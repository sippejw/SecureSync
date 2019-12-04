#! /usr/bin/python3

import urllib.request
import click
import os
import json
import socket
import sys
import glob
import hashlib
from random_word import RandomWords

@click.group()
def cli():
    pass


@click.command()
def init():
    if os.path.isfile('.SecureSync'):
        click.echo('This directory is already linked to a SecureSync instance!')
        return
    serverip = input('Please enter the server IP: ')
    generator = RandomWords()
    keys = generator.get_random_words(hasDictionaryDef="true", limit=5)
    keystring = "secure"
    for key in keys:
        keystring += "-" + key

    config = {
        "server": serverip,
        "dir": os.getcwd() + '/',
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
    serverip = input('Please enter the server IP: ')
    config = {
        'server': serverip,
        'dir': os.getcwd() + '/',
        'key': keystring
    }
    configfile = open(".SecureSync", "w+")
    configfile.write(json.dumps(config))
    configfile.close()
    click.echo("Connected!")


@click.command()
def sync():
    click.echo("Syncing!")
    try:
        configfile = open('.SecureSync', 'r')
        config = json.loads(configfile.read())
        configfile.close()
        ipaddr = config["server"]
        key = config["key"]
    except IOError:
        print('This directory is not linked to a SecureSync instance!')
        return
    fileState = getFiles(key)
    neededFiles = sendState(fileState, ipaddr)
    sendFiles(neededFiles, ipaddr)
    click.echo("Files have been sent!")

def getFiles(key):
    fileList = []
    ipaddr = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    for r, d, f in os.walk('.'):
        for file in f:
            if str(file) != '.SecureSync':
                fileList.append({'key': key, 'ip': ipaddr, 'filePath':os.path.join(r, file), 'fileHash':hashFile(os.path.join(r, file)), 'fileSize':os.path.getsize(os.path.join(r, file))})
    return fileList


def hashFile(filePath):
    BLOCKSIZE = 65536
    hasher = hashlib.md5()
    with open(filePath, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()

def sendState(state, ip):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 4000
    server.connect((ip, port))
    server.send(json.dumps(state).encode('utf-8'))
    neededFiles = json.loads(server.recv(2048))
    server.close()
    return neededFiles

def sendFiles(neededFiles, ip):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 4001
    server.connect((ip, port))
    for path in neededFiles:
        f = open(path, 'rb')
        while True:
            l = f.read(2048)
            while(l):
                server.send(l)
                l = f.read(2048)
            if not l:
                f.close()
                break
    return

cli.add_command(init)
cli.add_command(connect)
cli.add_command(sync)


if __name__ == '__main__':
    cli()
