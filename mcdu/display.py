from pyglet.text.document import UnformattedDocument
from pyglet.text.layout import TextLayout
from pyglet.window import key
import pyglet.resource

from mcdu.layout import Layout
import pyglet
import string

class Display(pyglet.window.Window):
    rows = []

    def __init__(self, mcdu, *args, **kwargs):
        self.mcdu = mcdu
        self.layout = Layout()

        bg_image = pyglet.resource.image("res/mcdu.png")
        self.bg = pyglet.sprite.Sprite(bg_image)

        for i in range(14):
            document = UnformattedDocument()
            text_layout = TextLayout(document)
            text_layout.y = 515 - i*15

            if not i % 2 or i == 13:
                document.set_style(0, 0, {
                        "font_name": "Inconsolata",
                        "font_size": 15,
                        "color": (80, 250, 80, 255),
                })
                text_layout.x = 64
            else:
                document.set_style(0, 0, {
                        "font_name": "Inconsolata",
                        "font_size": 11,
                        "kerning": 3.1,
                        "color": (80, 250, 80, 255),
                })
                text_layout.x = 61

            self.rows.append((document, text_layout))

        kwargs.update(dict(resizable=False, width=366, height=570, caption="MCDU"))
        pyglet.window.Window.__init__(self, *args, **kwargs)

    def row_write(self, index, text):
        self.rows[index][0].text = text

    def on_text(self, text):
        allowed = string.digits + string.ascii_uppercase + " /."
        text = str(text).upper()
        if text in allowed:
            self.mcdu.scratch_input(text)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.BACKSPACE:
            self.mcdu.scratch_delete()
        elif symbol == key.DELETE:
            self.mcdu.scratch_clear()

    def on_button_press(self, button):
        if len(button) == 1:
            self.mcdu.scratch_input(button)
        if button == "DEL":
            self.mcdu.scratch_delete()
        elif button == "CLR":
            self.mcdu.scratch_clear()
        elif button == "MENU":
            self.mcdu.menu()
        elif button.startswith("LSK") and len(button) == 5:
            side = 1 if button[4] == "R" else 0
            num = int(button[3])-1
            self.mcdu.lsk((num, side))

    def on_mouse_press(self, x, y, button, modifiers):
        for button in self.layout.buttons:
            if button[0][0] < x < button[1][0] and button[0][1] < y < button[1][1]:
                self.on_button_press(button[2])

    def on_draw(self):
        self.clear()
        self.bg.draw()
        for row in self.rows:
            row[1].draw()

if __name__ == "__main__":
    from mcdu import MCDU
    window = Window(mcdu)
    start()
