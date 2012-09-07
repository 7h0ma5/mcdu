from mcdu.subsystem import Subsystem
from mcdu.page import Page, Field

import time

class ATC(Subsystem):
    name = "ATC"

    def __init__(self, api):
        Subsystem.__init__(self)
        self.api = api
        self.midn = 0
        self.act = ""
        self.next = ""
        self.callsign = ""

    def run(self):
        i = 0
        while self.running:
            if not i % 10:
                self.fetch_messages()

            time.sleep(1)
            i = i + 1

    def fetch_messages(self):
        if not self.callsign: return
        messages = self.api.poll_cpdlc(self.callsign)

        for message in messages:
            self.parse_message(message)

    def parse_message(self, message):
        cpdlc = message[3].split("/")

        if cpdlc[1] != "data2": return

        midn = cpdlc[2]
        mrn = cpdlc[3]
        ra = cpdlc[4]
        msg = cpdlc[5]

        self.act = message[0]

        print midn, mrn, ra, msg

    def logon(self):
        self.send_message("", "Y", "REQUEST LOGON")

    def send_message(self, mrn, ra, msg):
        msg = "/data2/%i/%s/%s/%s" % (self.midn, mrn, ra, msg)
        self.api.cpdlc(self.callsign, self.act, msg)
        self.midn += 1

    def activate(self):
        self.mcdu.page_set(LogonPage)

class LogonPage(Page):
    title = "ATC LOGON"

    def init(self):
        self.field(0, "LOGON_TO", "_"*4, format=Field.icao, update=self.station)
        self.field(0, "STATUS", "LOGON>", action=self.logon)
        self.field(1, "FLT NO", "_"*7, format=Field.flightno, update=self.callsign)
        self.field(2, "ATC COMM", "<SELECT OFF", action=self.comm_off)
        self.field(2, "ACT CTR", "")
        self.field(3, "", "")
        self.field(3, "NEXT CTR", "")
        self.field(4, "ADS ARM", "<SELECT OFF", action=self.ads_arm)
        self.field(4, "ADS EMERG", "<SELECT ON", action=self.ads_emerg)
        self.field(5, "------------", "<INDEX", action=self.index)
        self.field(5, "------------", "")

    def station(self, value):
        self.sys.act = value

    def logon(self):
        self.sys.logon()

    def callsign(self, value):
        self.sys.callsign = value

    def comm_off(self):
        pass

    def ads_arm(self):
        pass

    def ads_emerg(self):
        pass

    def index(self):
        pass
