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
        """Alias for Window.get_width."""
        return self.get_width()

    @property
    def height(self) -> int:
        """Alias for Window.get_height."""
        return self.get_height()

    @property
    def size(self) -> tuple:
        """Alias for Window.get_size."""
        return self.get_size()

    def get_width(self) -> int:
        """Returns the widget of the window."""
        if self.surface:
            return self.surface.get_width()
        return self.initial_dimension[0]

    def get_height(self) -> int:
        """Returns the height of the window."""
        if self.surface:
            return self.surface.get_height()
        return self.initial_dimension[1]

    def get_size(self) -> tuple:
        """Returns the size of the size."""
        if self.surface:
            return self.surface.get_size()
        return self.initial_dimension

    def build(self):
        """Build the window."""
        self.surface = pygame.display.set_mode(self.initial_dimension)
        self.set_title(self.initial_title)

        return self
