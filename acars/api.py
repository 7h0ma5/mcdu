import urllib.parse
import urllib.request
import time

API_URL = "http://www.hoppie.nl/acars/system/connect.html"

class ACARS_API(object):
    def __init__(self, logon, avionics):
        self.logon = logon
        self.avionics = avionics

    def request(self, req_type, data={}):
        default_data = {
            "logon": self.logon,
            "to": "TEST",
            "type": req_type,
            "package": "",
        }

        default_data.update(data)
        params = urllib.parse.urlencode(default_data)
        path = "%s?%s" % (API_URL, params)

        res = urllib.request.urlopen(path)

        return res.read()

    def telex(self, callsign, receiver, message):
        data = {
            "from": callsign,
            "to": receiver,
            "packet": message,
        }
        return self.request("telex", data)

    def ads_c(self, callsign, receiver):
        package = [
            "REPORT",
            callsign,
            time.strftime("%d%H%M", time.gmtime()),
            str(self.avionics.pos[0]),
            str(self.avionics.pos[1]),
            str(self.avionics.alt),
            str(self.avionics.hdg),
            str(self.avionics.speed),
            self.avionics.wind,
            str(self.avionics.temp),
            "LVL",
        ]

        data = {
            "from": callsign,
            "to": receiver,
            "packet": " ".join(package),
        }

        return self.request("ads-c", data)
