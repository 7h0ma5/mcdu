from display import Display
from page import Page

class MCDU():
    def __init__(self):
        self.display = Display(self)
        self.scratch = ""
        self.subsystems = []
        self.sys = None

        self.clear()
        self.row_set(4, ["MCDU 1.0"])
        self.row_set(8, ["BY THOMAS GATZWEILER"])

    def subsystem_register(self, subsystem):
        subsystem.connect(self)
        self.subsystems.append(subsystem)

    def subsystem_unregister(self, subsystem):
        self.subsystems.remove(subsystem)

    def subsystem_activate(self, subsystem):
        self.sys = subsystem
        subsystem.activate()

    def clear(self):
        self.rows = [None for i in range(13)]
        self.render()

    def row_set(self, index, value):
        self.rows[index] = value
        self.row_render(index)

    def row_render(self, index):
        row = self.rows[index]

        if not row:
            text = ""
        elif len(row) == 1:
            text = str.center(row[0], 24)
        elif len(row) == 2:
            left = row[0]
            right = str.rjust(row[1], 24)
            text = left + right[len(left):24]
        else:
            text = ""

        self.display.row_write(index, text)

    def menu(self):
        self.page_set(MenuPage)

    def page_set(self, page):
        self.clear()
        self.page = page(self, self.sys)
        self.page.refresh()

    def lsk(self, pos):
        self.page.lsk(pos)

    def scratch_input(self, symbol):
        self.scratch += symbol
        self.scratch_update()

    def scratch_set(self, value):
        self.scratch = value
        self.scratch_update()

    def scratch_delete(self):
        if len(self.scratch) > 0:
            self.scratch = self.scratch[:-1]
            self.scratch_update()

    def scratch_clear(self):
        self.scratch_set("")

    def scratch_update(self):
        if (len(self.scratch) > 24):
            text = "<" + self.scratch[-23:]
        else:
            text = self.scratch

        self.display.row_write(13, text)

    def render(self):
        for i in range(len(self.rows)):
            self.row_render(i)

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
