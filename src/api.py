from __future__ import print_function
from twisted.internet import defer, reactor
import wormhole
import sys, os
from helpers.cmd import send, receive

app_id = "https://github.com/sippejw/SecureSync"
relay_url = "ws://relay.magic-wormhole.io:4000/v1"
RENDEZVOUS_RELAY = "ws://relay.magic-wormhole.io:4000/v1"
TRANSIT_RELAY = "tcp:transit.magic-wormhole.io:4001"
js_server = "tcp://127.0.0.1:4243"

class WormholeConfig(object):
    def __init__(self, code=None):
        self.appid = app_id
        self.relay_url = RENDEZVOUS_RELAY
        self.code = code
        self.code_length = 2
        self.text = None
        self.what = None
        self.dump_timing = None
        self.zeromode = False
        self.verify = False
        self.transit_helper = TRANSIT_RELAY
        self.listen = True
        self.output_file = ""
        self.accept_file = True
        self.tor = None
        self.launch_tor = False
        self.tor_control_port = ""
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.ignore_unsendable_files = False
        self.hide_progress = False
        self.timing = wormhole.timing.DebugTiming()
        self.cwd = os.getcwd()
        self.js_client = None

class WormholeAPI(object):
    def __init__(self):
        pass
    def send(self, code, path):
        arg = WormholeConfig(code)
        dirname = os.path.dirname(path)
        filename = os.path.basename(path)
        arg.what = filename
        arg.cwd = dirname
        res = send(arg)
        return res
    def receive(self, code):
        args = WormholeConfig(code)
        res = receive(args)
        return "received"
    def update_code(self, code):
        print("update code is {}".format(code))
        # self.client.updateCode(code)
    def echo(self, text):
        """echo any text"""
        return text
