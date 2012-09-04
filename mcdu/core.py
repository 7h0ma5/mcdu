from mcdu.display import Display
from mcdu.page import Page

class MCDU():
    def __init__(self):
        self.display = Display(self)
        self.sys = None
        self.page = None
        self.subsystems = []
        self.scratch = ""

        self.clear()
        self.row_set(4, ["MCDU 1.0"])
        self.row_set(8, ["BY THOMAS GATZWEILER"])

    def subsystem_register(self, subsystem):
        """Register and start the given subsystem."""
        self.subsystems.append(subsystem)
        subsystem.connect(self)
        subsystem.start()

    def subsystem_activate(self, subsystem):
        """Activate the given subsystem."""
        self.sys = subsystem
        subsystem.activate()

    def clear(self):
        """Clear the whole screen."""
        self.rows = [None for i in range(13)]
        self.render()

    def row_set(self, index, value):
        """Set a row. The index has to be between 0 and 12. The value
        has to contain a list with three strings at maximum.
        """
        self.rows[index] = value
        self.row_render(index)

    def row_render(self, index):
        """Write a row to the screen. If the row contains one string
        it will be centered. If it containes two strings the first
        will be left adjusted and the second will be right adjusted.
        """
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
        """Show the menu page."""
        self.page_set(MenuPage)

    def page_set(self, page):
        """Switch to the given page."""
        self.clear()
        self.page = page(self, self.sys)
        self.page.refresh()

    def lsk(self, pos):
        """Forward the pressed Line Select Key to the page."""
        if self.page: self.page.lsk(pos)

    def scratch_input(self, text):
        """Append a string to the scratchpad."""
        self.scratch += text
        self.scratch_update()

    def scratch_set(self, text):
        """Change the scratchpad to the given string."""
        self.scratch = text
        self.scratch_update()

    def scratch_delete(self):
        """Delete the last character of the scratchpad."""
        if len(self.scratch) > 0:
            self.scratch = self.scratch[:-1]
            self.scratch_update()

    def scratch_clear(self):
        """Clear the scratchpad."""
        self.scratch_set("")

    def scratch_update(self):
        """Write the scratchpad to the screen. If it contains more
        than 24 characters, only the last 24 characters are shown.
        """
        if (len(self.scratch) > 24):
            text = "<" + self.scratch[-23:]
        else:
            text = self.scratch

        self.display.row_write(13, text)

    def render(self):
        """Render all rows."""
        for i in range(len(self.rows)):
            self.row_render(i)

class MenuPage(Page):
    title = "MCDU MENU"

    def init(self):
        for i in range(len(self.mcdu.subsystems)):
            subsystem = self.mcdu.subsystems[i]
            self.field(i, "", "<" + subsystem.name)

    def lsk(self, pos):
        num, side = pos

        if num < len(self.mcdu.subsystems):
            sys = self.mcdu.subsystems[num]
            self.mcdu.subsystem_activate(sys)
