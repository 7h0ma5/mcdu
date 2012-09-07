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
        self.messages = []

    def run(self):
        i = 0
        while self.running:
            if not i % 10:
                self.progress_update()
                self.fetch_messages()

            time.sleep(1)
            i = i + 1

    def progress_update(self):
        if self.avionics.progress > len(self.progress):
            ptime = time.strftime("%H%MZ", time.gmtime())
            self.progress.append(ptime)
            if self.armed:
                self.report()

    def fetch_messages(self):
        if not self.flightno: return
        messages = self.api.poll_acars(self.flightno)
        messages.extend(self.messages)
        self.messages = messages
        print(messages)

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

    def inforeq(self, req, apt):
        self.api.inforeq(self.flightno, req, apt)

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
        self.sys.avionics.progress = 0
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
        self.mcdu.page_set(MessagesPage)

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
        self.mcdu.page_set(MessagesPage)

    def requests(self):
        self.mcdu.page_set(RequestsPage)

    def index(self):
        print("index")

    def postflight(self):
        self.sys.state = ACARS.postflight
        self.mcdu.page_set(PostflightPage)

class PostflightPage(Page):
    title = "ACARS POSTFLIGHT"

    def init(self):
        pass

class MessagesPage(Page):
    title = "ACARS MESSAGES"

    def init(self):
        self.field(5, "", "<RETURN", action=self.ret)

    def refresh(self):
        messages = self.sys.messages
        for i in range(5):
            self.fields[i] = None

            if i < len(messages):
                message = messages[i]
                self.field(i, message[0], message[2])
                self.field(i, "", message[1] + ">")

        Page.refresh(self)

    def lsk(self, pos):
        num, side = pos

        if num < 5 and num < len(self.sys.messages):
            self.mcdu.page_set(MessagePage)
            self.mcdu.page.message = self.sys.messages[num]
            self.mcdu.page.refresh()
        else:
            Page.lsk(self, pos)

    def ret(self):
        self.sys.activate()

class MessagePage(Page):
    title = "ACARS MESSAGE"

    def init(self):
        self.message = None
        self.field(5, "", "<RETURN", action=self.ret)

    def refresh(self):
        if self.message:
            text = self.message[3]

            for i in range(5):
                self.fields[i] = None
                self.field(i, "", text[i*24:(i+1)*24])

        Page.refresh(self)

    def ret(self):
        self.mcdu.page_set(MessagesPage)

class RequestsPage(Page):
    title = "ACARS REQUESTS"

    def init(self):
        self.field(0, "", "<ROUTE", action=self.route)
        self.field(0, "", "WEATHER>", action=self.weather)
        self.field(1, "", "<RELEASE", action=self.release)
        self.field(1, "", "ATIS>", action=self.atis)
        self.field(2, "", "<LOADSHEET", action=self.loadsheet)
        self.field(3, "", "<ARR INFO", action=self.arr_info)
        self.field(4, "", "")
        self.field(4, "SEND", "TELEX>", action=self.telex)
        self.field(5, "", "<RETURN", action=self.ret)

    def route(self):
        pass

    def weather(self):
        self.mcdu.page_set(WeatherRequestPage)

    def release(self):
        pass

    def atis(self):
        pass

    def loadsheet(self):
        pass

    def arr_info(self):
        pass

    def telex(self):
        pass

    def ret(self):
        self.sys.activate()

class WeatherRequestPage(Page):
    title = "ACARS WEATHER REQUEST"

    def init(self):
        self.field(0, "Airport", "_"*4, format=Field.icao, update=self.airport)
        self.field(3, "", "")
        self.field(3, "REQUEST", "METAR>", action=self.metar)
        self.field(4, "RECEIVED", "<MESSAGES", action=self.messages)
        self.field(4, "REQUEST", "TAF>", action=self.taf)
        self.field(5, "RETURN TO", "<REQUESTS", action=self.requests)
        self.field(5, "REQUEST", "SHORT TAF>", action=self.short_taf)

    def airport(self, value):
        self.apt = value

    def metar(self):
        self.sys.inforeq("metar", self.apt)

    def taf(self):
        self.sys.inforeq("taf", self.apt)

    def short_taf(self):
        self.sys.inforeq("shorttaf", self.apt)

    def requests(self):
        self.mcdu.page_set(RequestsPage)

    def messages(self):
        self.mcdu.page_set(MessagesPage)
