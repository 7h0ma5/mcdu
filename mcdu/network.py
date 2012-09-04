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
            "package": "",
        }

        default_data.update(data)
        params = urlencode(default_data)
        path = "%s?%s" % (API_URL, params)

        res = urlopen(path)

        return res.read().decode("utf-8")

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

        regex = "^ok \{server info \{(.*)\}\}$"
        match = re.match(regex, resp)

        if (match):
            self.messages.append(match.group(1))
