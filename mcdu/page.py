import re

class Page(object):
    _instance = None

    def __new__(cls, *args):
        if not cls._instance:
            cls._instance = super(Page, cls).__new__(cls, *args)

        return cls._instance

    def __init__(self, mcdu, sys):
        self.mcdu = mcdu
        self.sys = sys

        if not getattr(self, "rows", None):
            init = getattr(self, "init", None)
            if init:
                init()
            else:
                self.rows = [None for i in range(13)]

    def refresh(self):
        for i in range(len(self.rows)):
            self.mcdu.row_set(i, self.rows[i])

    def lsk(self, pos):
        side, num = pos
        row_index = num*2

        if row_index < len(self.mcdu.rows):
            row = self.mcdu.rows[row_index]

            if not row:
                return
            elif side == "right" and len(row) < 2:
                return
            elif side == "left":
                col_index = 0
            elif side == "right":
                col_index = len(row)-1

            if self.mcdu.scratch:
                try:
                    self.update_field((row_index, col_index), str(self.mcdu.scratch))
                except ValueError:
                    self.mcdu.scratch_set("INVALID FORMAT")
                else:
                    self.mcdu.row_render(row_index)
                    self.mcdu.scratch_clear()
            else:
                self.mcdu.scratch_set(row[col_index])

    def update_field(self, pos, value):
        self.rows[pos[0]][pos[1]] = value
        self.mcdu.rows[pos[0]][pos[1]] = value

    def validate(self, regex, value):
        if not re.match(regex, value):
            raise ValueError

    def validate_time(self, value):
        self.validate("^([01][0-9]|2[0-3])[0-5][0-9]Z$", value)

    def validate_icao(self, value):
        self.validate("^[A-Z]{4}$", value)
