#!/usr/bin/env python

import sys, pyglet

from mcdu.core import MCDU
from mcdu.acars import ACARS
from mcdu.atc import ATC
from mcdu.network import ACARS_API
from mcdu.avionics import Avionics, XPlaneReceiver

try:
    from configparser import SafeConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser

def run():
    config = SafeConfigParser()
    config.readfp(open("config/defaults.cfg"))
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
        mcdu.display.close()
        pyglet.app.exit()
        receiver.stop()
        sys.exit(0)

if __name__ == "__main__":
    run()
