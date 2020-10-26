import pygame


class Window:
    def __init__(self, title: str, dimension: tuple):
        self.surface = None

        self.initial_title = title
        self.dimension = dimension

    @property
    def title(self) -> str:
        """Returns the title of the window."""
        return pygame.display.get_caption()

    @title.setter
    def title(self, new_title: str):
        """Sets the window title."""
        pygame.display.set_caption(new_title)

    def set_title(self, new_title: str):
        """Alias for `Window.title = ...`."""
        self.title = new_title

    def build(self):
        """Build the window."""
        self.surface = pygame.display.set_mode(self.dimension)
        self.set_title(self.initial_title)

        return self
