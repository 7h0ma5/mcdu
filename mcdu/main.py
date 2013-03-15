#!/usr/bin/env python

from mcdu.core import MCDU
from mcdu.acars import ACARS
from mcdu.atc import ATC
from mcdu.network import ACARS_API
#from mcdu.xplane import XPlaneReceiver
from mcdu.fsx import FSXReceiver
from mcdu.websocket import WebSocket

import tornado.ioloop
import tornado.web

import os, sys, webbrowser

try:
    from configparser import SafeConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser

def run():
    config = SafeConfigParser()
    config.read("config/defaults.cfg")
    config.read("~/.config/mcdu.cfg")
    config.read("config/mcdu.cfg")

    #receiver = XPlaneReceiver()
    receiver = FSXReceiver()
    receiver.start()

    api = ACARS_API(config.get("ACARS", "logon"))
    acars = ACARS(api)
    atc = ATC(api)

    mcdu = MCDU()
    mcdu.subsystem_register(acars)
    mcdu.subsystem_register(atc)
    mcdu.menu()

    application = tornado.web.Application([
        (r"^/socket", WebSocket, dict(mcdu=mcdu)),
        (r"^/(.*)$", tornado.web.StaticFileHandler, {"path": "res/", "default_filename": "index.html"}),
    ], debug=False)

    port = config.getint("General", "port")
    application.listen(port)

    try:
        print("running on port %i" % port)
        webbrowser.open_new("http://localhost:%i" % port)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("quitting...")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("quitting...")
    finally:
        receiver.stop()
        acars.stop()
        atc.stop()
        sys.exit(0)

if __name__ == "__main__":
    run()
