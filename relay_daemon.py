#!/usr/bin/python

import sys
import os
import logging
import socket
import signal
import yaml
import sleekxmpp

# sleekxmpp wants this.
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')

logger = logging.getLogger("relay")

class XMPP(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, target):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping
        self.add_event_handler("session_start", self.start)
        self.target = target

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def send_target_message(self, message):
        self.send_message(mto=self.target, mbody=message, mtype='chat')

class Sock(object):
    def __init__(self, path, xmpp):
        self.path = path
        self.xmpp = xmpp

        if os.access(path, os.F_OK):
            os.unlink(path)
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.sock.bind(path)

    def try_unicode(self, text):
        for enc in ["ascii", "utf8", "iso-8859-1", "windows-1252"]:
            try:
                return unicode(text, enc)
            except:
                pass

        return unicode(text, "ascii", "ignore")

    def run(self):
        while True:
            msg, peer = self.sock.recvfrom(10024)
            msg = self.try_unicode(msg)
            self.xmpp.send_target_message(msg)

    def close(self):
        self.sock.close()
        os.unlink(sock.path)

def detach_process():
    # Fork
    if os.fork() > 0:
        os._exit(0)

    # Detach
    os.setsid()

    null_fd = os.open(os.devnull, os.O_RDWR)
    for s in [sys.stdin, sys.stdout, sys.stderr]:
        os.dup2(null_fd, s.fileno())

    # Fork
    if os.fork() > 0:
        os._exit(0)

def kill(xmpp, sock):
    signal.alarm(30)
    logger.info("Signal: shutting down")
    xmpp.disconnect(wait=True)
    sock.close()
    logger.debug("Shutdown done")
    raise SystemExit

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: {0} config.yml".format(sys.argv[0])
        sys.exit(1)

    with open(sys.argv[1]) as f:
        config = yaml.load(f)

    logconfig = config.get('logging', {})
    if "format" not in logconfig:
        logconfig["format"] = \
                "%(asctime)s %(levelname)s %(name)s %(message)s"
    if "level" in logconfig:
        logconfig["level"] = getattr(logging, logconfig["level"])
    logging.basicConfig(**logconfig)

    xmpp = XMPP(config["jid"], config["password"], config["target"])
    sock = Sock(config["socket"], xmpp)

    if "fork" in config and config["fork"]:
        detach_process()

    for s in [signal.SIGTERM, signal.SIGINT]:
        signal.signal(s, lambda s, f: kill(xmpp, sock))

    xmpp.connect()
    xmpp.process(block=False)
    sock.run()
