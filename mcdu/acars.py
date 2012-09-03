from mcdu.subsystem import Subsystem
from mcdu.avionics import Avionics
from mcdu.page import Page, Field

import time

class ACARS(Subsystem):
    name = "ACARS"

    preflight = 1
    inflight = 2
    postflight = 3

    def __init__(self, api):
        Subsystem.__init__(self)
        self.api = api
        self.avionics = Avionics()
        self.state = ACARS.preflight

        self.armed = False
        self.flightno = ""
        self.origin = ""
        self.dest = ""
        self.plan_dep = ""
        self.eta = ""
        self.altrnt = ""
        self.company = ""
        self.progress = []

    def run(self):
        while True:
            if self.avionics.progress > len(self.progress):
                ptime = time.strftime("%H%MZ", time.gmtime())
                self.progress.append(ptime)
                if self.armed:
                    self.report()

            time.sleep(10)

    def activate(self):
        if self.state == ACARS.preflight:
            self.mcdu.page_set(PreflightPage)
        elif self.state == ACARS.inflight:
            self.mcdu.page_set(InflightPage)
        elif self.state == ACARS.postflight:
            self.mcdu.page_set(PostflightPage)

    def report(self):
        message = ["%s/%s" % (self.origin, self.dest)]

        if len(self.progress) > 0:
            message.append("OUT/" + self.progress[0])

        if len(self.progress) > 1:
            message.append("OFF/" + self.progress[1])

        if len(self.progress) > 2:
            message.append("ON/" + self.progress[2])

        if len(self.progress) > 3:
            message.append("IN/" + self.progress[3])

        if len(self.progress) < 3 and self.eta:
            message.append("ETA/" + self.eta)

        self.api.progress(self.flightno, self.company, " ".join(message))

class PreflightPage(Page):
    title = "ACARS PREFLIGHT"

    def init(self):
        self.field(0, "SYSTEM INIT", "<ARM", action=self.arm)
        self.field(0, "FLT NO", "_"*7, format=Field.flightno, update=self.flightno)
        self.field(1, "ORIGIN", "_"*4, format=Field.icao, update=self.origin)
        self.field(1, "PLAN DEP", "_"*5, format=Field.time, update=self.plan_dep)
        self.field(2, "DEST", "_"*4, format=Field.icao, update=self.dest)
        self.field(2, "ETA", "_"*5,  format=Field.time, update=self.eta)
        self.field(3, "ALTRNT", "_"*4, format=Field.icao, update=self.altrnt)
        self.field(3, "COMPANY", "___", format="^[A-Z]{3}$", update=self.company)
        self.field(4, "RECEIVED", "<MESSAGES", action=self.messages)
        self.field(4, "", "REQUESTS>", action=self.requests)
        self.field(5, "ACARS", "<INDEX", action=self.index)
        self.field(5, "", "INFLIGHT>", action=self.inflight)

    def arm(self):
        self.avionics.progress = 0
        self.sys.armed = True
        self.field_update(0, 0, "ARMED")

    def flightno(self, value):
        self.sys.flightno = value

    def origin(self, value):
        self.sys.origin = value

    def plan_dep(self, value):
        self.sys.plan_dep = value

    def dest(self, value):
        self.sys.dest = value

    def eta(self, value):
        self.sys.eta = value

    def altrnt(self, value):
        self.sys.altrnt = value

    def company(self, value):
        self.sys.company = value

    def messages(self):
        print("messages")

    def requests(self):
        self.mcdu.page_set(RequestsPage)

    def index(self):
        print("index")

    def inflight(self):
        self.sys.state = ACARS.inflight
        self.mcdu.page_set(InflightPage)

class InflightPage(Page):
    title = "ACARS INFLIGHT"

    def init(self):
        self.field(0, "POSITION", "<REPORT", action=self.report)
        self.field(0, "ETA", self.sys.eta, format=Field.time, update=self.eta)
        self.field(1, "DEVIATE", self.sys.altrnt, format=Field.icao, update=self.deviate)
        self.field(4, "RECEIVED", "<MESSAGES", action=self.messages)
        self.field(4, "", "REQUESTS>", action=self.requests)
        self.field(5, "ACARS", "<INDEX", action=self.index)
        self.field(5, "", "POSTFLIGHT>", action=self.postflight)

    def report(self):
        self.sys.report()

    def eta(self, value):
        self.sys.eta = value

    def deviate(self, value):
        self.sys.altrnt = value

    def messages(self):
        print("messages")

    def requests(self):
        self.mcdu.page_set(RequestsPage)
        print("requests")

    def index(self):
        print("index")

    def postflight(self):
        self.sys.state = ACARS.postflight
        self.mcdu.page_set(PostflightPage)

class PostflightPage(Page):
    title = "ACARS POSTFLIGHT"

    def init(self):
        pass

class RequestsPage(Page):
    title = "ACARS REQUESTS"

    def init(self):
        pass
