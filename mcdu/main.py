#!/usr/bin/env python

from mcdu.core import MCDU
from mcdu.acars import ACARS
from mcdu.atc import ATC
from mcdu.network import ACARS_API
from mcdu.xplane import XPlaneReceiver

import os, sys, pyglet
import pyglet.resource

try:
    from configparser import SafeConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser

def run():
    pyglet.resource.path.append(os.getcwd())
    pyglet.resource.path.append("/usr/share/mcdu")
    pyglet.resource.path.append("/usr/local/share/mcdu")
    pyglet.resource.reindex()

    config = SafeConfigParser()
    config.readfp(pyglet.resource.file("config/defaults.cfg", "r"))
    config.read("~/.config/mcdu.cfg")
    config.read("config/mcdu.cfg")

    receiver = XPlaneReceiver()
    receiver.start()

    api = ACARS_API(config.get("ACARS", "logon"))
    acars = ACARS(api)
    atc = ATC(api)

    mcdu = MCDU()
    mcdu.subsystem_register(acars)
    mcdu.subsystem_register(atc)

    try:
        pyglet.app.run()
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
        mcdu.display.close()
        pyglet.app.exit()
        sys.exit(0)

if __name__ == "__main__":
    run()
