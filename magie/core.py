import pygame

import traceback

from . import abc, window
from .enumerations import State, Colors

pygame.init()


class Magie(abc.Capsule, abc.Widget):
    def __init__(self, width: int, height: int, fps: int = 60):
        super().__init__()
        abc.Widget.__init__(self, state=State.DISABLED)

        self.window = window.Window("Magie", (width, height))
        self.fps = fps

    def dispath(self, name, *args):
        for listener in self.listeners.get("on_" + name, ()):
            listener(*args)

    def _event_handler(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            self.dispath("keydown", key)
        elif event.type == pygame.KEYUP:
            key = pygame.key.name(event.key)
            self.dispath("keyup", key)

    def build(self):
        window = self.window.build()

        tick = 0
        clock = pygame.time.Clock()

        self.enable()
        while self.state == State.ENABLED:
            window.surface.fill(Colors.BLACK.value)

            tick += clock.tick(self.fps)

            for timer in self.timers:
                if timer.state != State.ENABLED:
                    continue

                timer._next(tick)

            for event in pygame.event.get():
                self._event_handler(event)

            for drawable in self.drawables.values():
                if drawable.state != State.ENABLED:
                    continue

                try:
                    drawable.draw(window.surface)
                except Exception:
                    drawable.state = State.WARNING
                    traceback.print_exc()

            pygame.display.flip()
