import pygame


class Window:
    def __init__(self, title: str, dimension: tuple):
        self.surface = None

        self.initial_title = title
        self.initial_dimension = dimension

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

    @property
    def width(self) -> int:
        """Returns the widget of the window."""
        w, _ = pygame.display.get_window_size()
        return w

    @property
    def height(self) -> int:
        """Returns the height of the window."""
        _, h = pygame.display.get_window_size()
        return h

    @property
    def size(self) -> tuple:
        """Returns the size of the window."""
        return pygame.display.get_window_size()

    def build(self):
        """Build the window."""
        self.surface = pygame.display.set_mode(self.initial_dimension)
        self.set_title(self.initial_title)

        return self
