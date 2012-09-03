import threading

class Subsystem(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def connect(self, mcdu):
        self.running = True
        self.mcdu = mcdu

    def stop(self):
        self.running = False
