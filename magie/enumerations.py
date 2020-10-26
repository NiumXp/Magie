import enum


class State(enum.IntEnum):
    ENABLED = 0
    DISABLED = 1
    WARNING = 3


class Colors(enum.Enum):
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
