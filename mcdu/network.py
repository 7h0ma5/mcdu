try:
    from urllib.parse import urlencode
    from urllib.request import urlopen
except ImportError:
    from urllib import urlencode
    from urllib2 import urlopen

import re

API_URL = "http://www.hoppie.nl/acars/system/connect.html"

class ACARS_API(object):
    def __init__(self, logon):
        self.logon = logon
        self.messages = []

    def request(self, req_type, data={}):
        default_data = {
            "logon": self.logon,
            "to": "TEST",
            "type": req_type,
            "packet": "",
        }

        default_data.update(data)
        params = urlencode(default_data)
        path = "%s?%s" % (API_URL, params)

        res = urlopen(path)

        return res.read().decode("utf-8")

    def parse_messages(self, data):
        if not data.startswith("ok") or len(data) < 3:
            return None

        regex = "\{([a-zA-Z0-9]+) ([a-z\-]+) \{(.*?)\}\}"

        for match in re.finditer(regex, data):
            message = (match.group(2), match.group(1), match.group(3))
            self.messages.append(message)

    def poll(self, callsign):
        data = {
            "from": callsign,
            "to": "SERVER",
        }

        res = self.request("poll", data)
        self.parse_messages(res)

    def poll_acars(self, callsign):
        self.poll(callsign)

        acars = []

        for message in self.messages:
            if message[0] in ["telex", "metar", "taf", "shorttaf", "ads-c"]:
                acars.append(message)

        return acars

    def telex(self, callsign, receiver, message):
        data = {
            "from": callsign,
            "to": receiver,
            "packet": message,
        }
        self.request("telex", data)

    def progress(self, callsign, receiver, message):
        data = {
            "from": callsign,
            "to": receiver,
            "packet": message,
        }
        self.request("progress", data)

    def inforeq(self, callsign, req, apt):
        data = {
            "from": callsign,
            "to": "SERVER",
            "packet": "%s %s" % (req, apt)
        }
        resp = self.request("inforeq", data)

        regex = "^ok \{server info \{(.*)\}\}"
        match = re.match(regex, resp)

        if (match):
            self.messages.append(match.group(1))
