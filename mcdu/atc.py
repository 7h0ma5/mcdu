from mcdu.subsystem import Subsystem

class ATC(Subsystem):
    name = "ATC"

    def __init__(self, avionics):
        Subsystem.__init__(self)
        self.avionics = avionics

    def activate(self):
        print("activate!")
