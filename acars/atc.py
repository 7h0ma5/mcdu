from mcdu.subsystem import Subsystem

class ATC(Subsystem):
    name = "ATC"

    def __init__(self, avionics, api):
        Subsystem.__init__(self)
        self.avionics = avionics
        self.api = api

    def activate(self):
        print("activate!")
