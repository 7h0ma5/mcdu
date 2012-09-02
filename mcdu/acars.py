from mcdu.subsystem import Subsystem
from mcdu.page import Page, Field

class ACARS(Subsystem):
    name = "ACARS"

    preflight = 1
    inflight = 2
    postflight = 3

    def __init__(self, api):
        Subsystem.__init__(self)
        self.api = api
        self.state = ACARS.preflight

        self.flightno = ""
        self.origin = ""
        self.dest = ""
        self.plan_dep = ""
        self.eta = ""
        self.altrnt = ""
        self.company = ""

    def activate(self):
        if self.state == ACARS.preflight:
            self.mcdu.page_set(PreflightPage)
        elif self.state == ACARS.inflight:
            self.mcdu.page_set(InflightPage)
        elif self.state == ACARS.postflight:
            self.mcdu.page_set(PostflightPage)

    def report(self):
        print(self.api.ads_c(self.flightno, self.company))

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
        print("arm!")
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
        print("requests")

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
