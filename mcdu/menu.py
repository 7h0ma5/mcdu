from .page import Page

class MenuPage(Page):
    title = "MCDU MENU"

    def init(self):
        self.rows = [[self.title]]

        for i in range(len(self.mcdu.subsystems)):
            subsystem = self.mcdu.subsystems[i]
            self.rows.append(None)
            self.rows.append(["<" + subsystem.name, ""])

        for i in range(len(self.rows), 13):
            self.rows.append(None)

    def lsk(self, pos):
        side, num = pos

        if num-1 < len(self.mcdu.subsystems):
            sys = self.mcdu.subsystems[num-1]
            self.mcdu.subsystem_activate(sys)
