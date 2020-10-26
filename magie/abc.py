import pygame

import abc
import collections
import typing

from .enumerations import State, Colors


class Widget(abc.ABC):
    """
    Parameters
    ----------
    state: magie.enumerations.State
        State of the Widget.

    Attributes
    ----------
    state : magie.enumerations.State
        State of the Widget.
    """
    def __init__(self, *, state: typing.Optional[State] = None):
        self.state = state if state is not None else State.DISABLED
        # `self.state` "puxa" pelo `__get__` do `property` `state` e ao
        # utilizar `self.state =`, ao invés do `__get__`, o `__set__` é
        # puxado e assim reutilizamos o código escrito e definimos lá
        # `self.__state`.

    @property
    def state(self) -> State:
        """Returns the state of the widget."""
        return self.__state

    @state.setter
    def state(self, new_state: State):
        if type(new_state) is not State:
            raise TypeError("State expected")
        try:
            self.on_state_change(self.__state, new_state)
        except AttributeError:
            pass
        self.__state = new_state

    def on_state_change(self, before, after):
        pass

    def enable(self) -> None:
        """Changes the state of the object to `State.ENABLED`."""
        self.__state = State.ENABLED

    def disable(self) -> None:
        """Changes the state of the object to `State.DISABLED`."""
        self.__state = State.DISABLED


def is_drawable(obj) -> bool:
    if issubclass(obj.__class__, Widget):
        function = getattr(obj, "draw", None)
        if callable(function):
            return True
    return False


class Timer(Widget):
    """
    Parameters
    ----------
    interval : int
        Interval of timer in *seconds*.
    target : typing.Callable
        Callable that will be called when interval is over.
    loop : typing.Optional[bool] (False)
        If the timer will be running infinitely.
    state : typing.Optional[magie.State]
        State of timer.
    """
    def __init__(self, interval: int, target: typing.Callable, *,
                 loop: bool = False, state=None):
        super().__init__(state=state)

        self._interval = interval * 1000
        self._next_tick = self._interval

        # __self__ = getattr(target, "__self__", None)
        # if __self__ is not None:
        #     target = lambda timer: target(__self__, timer)
        self._target = target

        self._loop = loop

        self.stopped = False

    def _next(self, tick: int):
        if not self.stopped:
            if tick >= self._next_tick:
                self._target(self)
                self.reset(tick)
            if not self._loop:
                self.stopped = True
                return
        else:
            if self._loop:
                self.stopped = False
                self.reset(tick)

    def reset(self, tick):
        """Reset the timer."""
        self._next_tick = tick + self._interval

    def stop(self):
        """Stop the timer."""
        self._loop = False
        self.stopped = True


class Capsule(abc.ABC):
    def __init__(self):
        # self.__timers = collections.defaultdict(list)
        self.__timers = list()
        self.__listeners = collections.defaultdict(list)
        self.__drawables = collections.OrderedDict()

    @property
    def timers(self):
        """Returns the timers of the object."""
        return self.__timers

    @property
    def listeners(self):
        """Returns the listeners of the object."""
        return self.__listeners

    @property
    def drawables(self) -> collections.OrderedDict:
        """Returns the drawables of the object."""
        return self.__drawables

    def extend(self, capsule):
        if issubclass(capsule.__class__, self.__class__):
            raise TypeError("magie.abc.Capsule expected")

        try:
            self.add_drawable(capsule)
        except TypeError:
            pass

        self.__timers.extend(capsule.timers)
        self.__listeners.update(capsule.listeners)
        self.__drawables.update(capsule.drawables)

    def add_timer(self, timer, *, enable: bool = False):
        """
        Add a timer.

        Parameters
        ----------
        timer : typing.Union[magie.abc.Timer, typing.Callable]
        enable : bool

        Raises
        ------
        TypeError
            Invalid type for `timer` parameter.
        """
        is_subclass_of_timer = issubclass(timer.__class__, Timer)
        if callable(timer) and not is_subclass_of_timer:
            timer = Timer.from_callable(timer)
        elif not is_subclass_of_timer:
            raise TypeError("magie.abc.Timer or callable expected")
        if enable:
            timer.state = State.ENABLED
        self.__timers.append(timer)

    def add_listener(self, listener, *, enable: bool = False) -> str:
        """
        Add a listener.

        Parameters
        ----------
        listener : typing.Callable

        Returns
        -------
        target : str
            The name of event that `listener` is listening.

        Raises
        ------
        TypeError
            `listener` is not a callable.
        """
        if not callable(listener):
            raise TypeError(f"{listener} is not a callable")
        try:
            name = listener.target
        except AttributeError:
            name = listener.__name__
        self.__listeners[name].append(listener)
        return name

    def add_drawable(self, drawable, *, enable: bool = False) -> typing.Any:
        """
        Add a drawable.

        Parameters
        ----------
        drawable : magie.abc.Drawable
        enable : bool

        Returns
        -------
        typing.Any
            Name of the drawable.

        Raises
        ------
        TypeError
            Invalid type for `drawable` parameter.
        NameError
            The name of `drawable` is already registred/used.
        """
        if not is_drawable(drawable):
            raise TypeError("magie.abc.Drawable expected")
        if not drawable.name:
            drawable.__name = f"Drawable:{len(self.__drawables)}"
        if self.__drawables.get(drawable.name, False):
            raise NameError(f"name '{drawable.name}' already exists")
        if enable:
            drawable.enable()
        self.__drawables[drawable.name] = drawable
        return drawable.name


class Drawable(Widget, Capsule):
    def __init__(self, name: typing.Optional[str] = None, *, state=None):
        super().__init__(state=state)
        Capsule.__init__(self)

        self.__name = name

    @property
    def name(self) -> str:
        """Returns the name of the drawable."""
        return self.__name

    @abc.abstractmethod
    def draw(self, surface):
        """Draw the object."""
        pass


class Font:
    def __init__(self, path: str, size: int, *, is_system: bool = False):
        if is_system:
            self.__font = pygame.sysfont.SysFont(path, size)
        else:
            self.__font = pygame.font.Font(path, size)

    @classmethod
    def get_default_font(cls, size: int):
        name = pygame.font.get_default_font()
        return cls(name, size, is_system=True)

    def render(self, text: str, color: tuple):
        if type(color) is Colors:
            color = color.value
        return self.__font.render(text, False, color)
