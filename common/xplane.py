import threading
import socket
import struct

class Receiver(threading.Thread):
    def __init__(self, avionics):
        threading.Thread.__init__(self)
        self.avionics = avionics
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(2)

        self.active = True

    def run(self):
        self.sock.bind(("", 49003))

        while self.active:
            try:
                data, addr = self.sock.recvfrom(1024)
                self.parse(data)
            except socket.timeout:
                pass

    def stop(self):
        self.active = False
        self.sock.close()

    def parse(self, data):
        header = struct.unpack("5s", data[:5])
        data = data[5:]

        for i in range(0, len(data), 36):
            packet = struct.unpack("i8f", data[i:i+36]);

            if packet[0] == 3:
                self.avionics.speed = int(round(packet[4]))
            elif packet[0] == 5:
                wind_heading = int(round(packet[5]))
                wind_speed = int(round(packet[4]))
                self.avionics.wind = "%i/%i" % (wind_heading, wind_speed)
            elif packet[0] == 6:
                self.avionics.temp = int(round(packet[2]))
            elif packet[0] == 17:
                self.avionics.hdg = int(round(packet[3]))
            elif packet[0] == 20:
                self.avionics.pos = (round(packet[1], 8), round(packet[2], 8))
                self.avionics.alt = int(round(packet[3]))
