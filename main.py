#!/usr/bin/env python

from acars.acars import ACARS
from acars.atc import ATC
from mcdu.mcdu import MCDU

import acars.api
import common.xplane
import common.avionics

import sys, pyglet

try:
    from configparser import SafeConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser

if __name__ == "__main__":
    config = SafeConfigParser()
    config.readfp(open("config/defaults.cfg"))
    config.read("config/mcdu.cfg")

    avionics = common.avionics.Avionics()

    receiver = common.xplane.Receiver(avionics)
    receiver.start()

    api = acars.api.ACARS_API(config.get("ACARS", "logon"), avionics)
    acars = ACARS(avionics, api)
    atc = ATC(avionics, api)

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
