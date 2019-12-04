#! /usr/bin/python3

import socket 
import select 
import sys 
import json
import os
import hashlib
import urllib.request

def hashFile(filePath):
    BLOCKSIZE = 65536
    hasher = hashlib.md5()
    with open(filePath, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
fileServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
configfile = open('.SecureSync', 'r')
config = json.loads(configfile.read())
configfile.close()
ip = config['server']
rootDir = config['dir']
port = 4000
server.connect((ip, port))
fileServer.connect((ip, 4001))
fileCount = 0
while True:
    test = server.recv(2048)
    state = json.loads(test)
    if state[0]['ip'] == urllib.request.urlopen('https://ident.me').read().decode('utf8'):
        fileSize = 0
        for f in state:
            fileSize += f['fileSize']
        fileServer.recv(fileSize)
    else:
        neededFiles = []
        fileSizes = []
        for f in state:
            if not os.path.isfile(rootDir + f['filePath']):
                neededFiles.append(f['filePath'])
                fileSizes.append(f['fileSize'])
            elif hashFile(rootDir + f['filePath']) != f['fileHash']:
                neededFiles.append(f['filePath'])
                fileSizes.append(f['fileSize'])
        files = zip(neededFiles, fileSizes)
        server.send(json.dumps(neededFiles).encode('utf-8'))
        for fs in files:
            dirPath = fs[0][:fs[0].rfind('/')]
            if not os.path.isdir(rootDir + dirPath):
                    os.mkdir(rootDir + dirPath)
            with open(rootDir + fs[0], 'w+') as f:
                    data = fileServer.recv(fs[1])
                    f.write(data.decode('utf-8'))
server.close()
            
