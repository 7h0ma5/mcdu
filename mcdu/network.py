try:
    from urllib.parse import urlencode
    from urllib.request import urlopen
except ImportError:
    from urllib import urlencode
    from urllib2 import urlopen

from mcdu.avionics import Avionics
import time

API_URL = "http://www.hoppie.nl/acars/system/connect.html"

class ACARS_API(object):
    def __init__(self, logon):
        self.logon = logon

    def request(self, req_type, data={}):
        default_data = {
            "logon": self.logon,
            "to": "TEST",
            "type": req_type,
            "package": "",
        }

        default_data.update(data)
        params = urlencode(default_data)
        path = "%s?%s" % (API_URL, params)

        res = urlopen(path)

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
            str(Avionics.pos[0]),
            str(Avionics.pos[1]),
            str(Avionics.alt),
            str(Avionics.hdg),
            str(Avionics.speed),
            Avionics.wind,
            str(Avionics.temp),
            "LVL",
        ]

        data = {
            "from": callsign,
            "to": receiver,
            "packet": " ".join(package),
        }

        return self.request("ads-c", data)
