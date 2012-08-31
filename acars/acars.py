from mcdu.subsystem import Subsystem
from mcdu.page import Page

class ACARS(Subsystem):
    name = "ACARS"

    def __init__(self, avionics, api):
        Subsystem.__init__(self)
        self.avionics = avionics
        self.api = api
        self.state = "preflight"

        self.flightno = ""
        self.origin = ""
        self.dest = ""
        self.plan_dep = ""
        self.eta = ""
        self.alternt = ""
        self.company = ""

    def activate(self):
        if self.state == "preflight":
            self.mcdu.page_set(PreflightPage)
        elif self.state == "inflight":
            self.mcdu.page_set(InflightPage)
        elif self.state == "postflight":
            self.mcdu.page_set(PostflightPage)

    def report(self):
        print(self.api.ads_c(self.flightno, self.company))

class PreflightPage(Page):
    title = "ACARS PREFLIGHT"

    def init(self):
        self.rows = [
            [self.title],
            ["SYSTEM INIT", "FLT NO"],
            ["<ARM", "_______"],
            ["ORIGIN", "PLAN DEP"],
            ["____", "_____"],
            ["DEST", "ETA"],
            ["____", "_____"],
            ["ALTRNT", "COMPANY"],
            ["____", "___"],
            ["RECEIVED", ""],
            ["<MESSAGES", "REQUESTS>"],
            ["ACARS", ""],
            ["<INDEX", "INFLIGHT>"],
        ]

    def lsk(self, pos):
        if pos == ("left", 6):
            print("index!")
        elif pos == ("right", 6):
            self.sys.state = "inflight"
            self.mcdu.page_set(InflightPage)
        else:
            Page.lsk(self, pos)

    def update_field(self, pos, value):
        if pos == (2, 1):
            self.validate("^[A-Z]{3}[0-9A-Z]{1,4}$", value)
            self.sys.flightno = value

        elif pos == (4, 0):
            self.validate_icao(value)
            self.sys.origin = value

        elif pos == (4, 1):
            self.validate_time(value)
            self.sys.plan_dep = value

        elif pos == (6, 0):
            self.validate_icao(value)
            self.sys.dest = value

        elif pos == (6, 1):
            self.validate_time(value)
            self.sys.eta = value

        elif pos == (8, 0):
            self.validate_icao(value)
            self.sys.alternt = value

        elif pos == (8, 1):
            self.validate("^[A-Z]{3}$", value)
            self.sys.company = value

        else:
            return

        Page.update_field(self, pos, value)


class InflightPage(Page):
    title = "ACARS INFLIGHT"

    def init(self):
        self.rows = [
            [self.title],
            ["POSITION", "ETA"],
            ["<REPORT", self.sys.eta],
            ["DEVIATE", ""],
            [self.sys.alternt, ""],
            None,
            None,
            None,
            None,
            ["RECEIVED", ""],
            ["<MESSAGES", "REQUESTS>"],
            ["ACARS", ""],
            ["<INDEX", "POSTFLIGHT>"],
        ]

    def lsk(self, pos):
        if pos == ("left", 1):
            self.sys.report()
        elif pos == ("left", 6):
            print("index!")
        elif pos == ("right", 6):
            self.sys.state = "postflight"
            self.mcdu.page_set(PostflightPage)
        else:
            Page.lsk(self, pos)

class PostflightPage(Page):
    title = "ACARS POSTFLIGHT"

    def init(self):
        self.rows = [
            [self.title],
            ["POSITION", "ETA"],
            ["<REPORT", self.sys.eta],
            ["DEVIATE", ""],
            [self.sys.alternt, ""],
            None,
            None,
            None,
            None,
            ["RECEIVED", ""],
            ["<MESSAGES", "REQUESTS>"],
            ["ACARS", ""],
            ["<INDEX", ""],
        ]
