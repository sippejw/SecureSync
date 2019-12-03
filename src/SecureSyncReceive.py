import socket 
import select 
import sys 
import json
import os
import hashlib

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
    state = json.loads(server.recv(2048))
    neededFiles = []
    fileSizes = []
    print(json.dumps(state))
    for f in state:
        print(f['filePath'])
        if not os.path.isfile(rootDir + f['filePath']):
            neededFiles.append(f['filePath'])
            fileSizes.append(f['fileSize'])
        elif hashFile(rootDir + f['filePath']) != f['fileHash']:
            neededFiles.append(f['filePath'])
            fileSizes.append(f['fileSize'])
    files = zip(neededFiles, fileSizes)
    server.send(json.dumps(neededFiles).encode('utf-8'))
    for fs in files:
        print(fs[0])
        dirPath = fs[0][:fs[0].rfind('/')]
        if not os.path.isdir(rootDir + dirPath):
                os.mkdir(rootDir + dirPath)
        with open(rootDir + fs[0], 'w+') as f:
                data = fileServer.recv(fs[1])
                f.write(data.decode('utf-8'))
server.close()
            
