from . import abc
from .enumerations import Colors


class Text(abc.Drawable):
    def __init__(self, text=None, *, position, font,
                 color=Colors.WHITE, name=None, state=None):
        super().__init__(name, state=state)

        self.initial_text = text
        self.position = position
        self.font = font
        self.color = color

    @property
    def text(self):
        return self.initial_text

    def draw(self, surface):
        source = self.font.render(self.text, self.color)
        surface.blit(source, self.position)
