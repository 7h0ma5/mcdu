from mcdu.subsystem import Subsystem
from mcdu.page import Page, Field

class ATC(Subsystem):
    name = "ATC"

    def __init__(self, mcdu):
        Subsystem.__init__(self)
        self.mcdu = mcdu

    def activate(self):
        self.mcdu.page_set(LogonPage)

class LogonPage(Page):
    title = "ATC LOGON"

    def init(self):
        self.field(0, "LOGON_TO", "_"*4, format=Field.icao, update=self.logon)
        self.field(0, "STATUS", "NOT SENT")
        self.field(1, "FLT NO", "_"*7, format=Field.flightno, update=self.flightno)
        self.field(2, "ATC COMM", "<SELECT OFF", action=self.comm_off)
        self.field(2, "ACT CTR", "")
        self.field(3, "", "")
        self.field(3, "NEXT CTR", "")
        self.field(4, "ADS ARM", "<SELECT OFF", action=self.ads_arm)
        self.field(4, "ADS EMERG", "<SELECT ON", action=self.ads_emerg)
        self.field(5, "------------", "<INDEX", action=self.index)
        self.field(5, "------------", "")

    def logon(self, value):
        pass

    def flightno(self, value):
        pass

    def comm_off(self):
        pass

    def ads_arm(self):
        pass

    def ads_emerg(self):
        pass

    def index(self):
        pass
