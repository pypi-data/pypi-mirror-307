from dataclasses import dataclass, Field, field
from typing import Callable

from ratisbona_pygames.gameutils import GameElement, PYGAME_KEYCODE, Game


@dataclass
class KeyPressBasedTimer(GameElement):
    game: Game
    keys: list[PYGAME_KEYCODE] = field(default_factory=list)
    then_callback: Callable[[PYGAME_KEYCODE], None] | None = None
    repeat_callback: Callable[[], None] | None = None
    dead_time_frames: int = 0

    def tick(self):
        if self.dead_time_frames > 0:
            self.dead_time_frames -= 1
            return

        for key in self.keys:
            if self.game.keys[key]:
                self.repeat_callback = None
                if self.then_callback is not None:
                    self.dead_time_frames = 30
                    self.then_callback(key)
                return


    def render(self):
        if self.repeat_callback is not None:
            self.repeat_callback()



@dataclass
class FrameBasedTimer(GameElement):
    remaining: int = 0
    repeat_callback: Callable[[], None] | None = None
    then_callback: Callable[[], None] | None = None

    def repeat(
            self,
            repeat: Callable[[], None] | None,
            for_num_frames: int,
            and_then: Callable[[], None] | None = None
    ):
        self.repeat_callback = repeat
        self.then_callback = and_then
        self.remaining = for_num_frames

    def tick(self):
        if self.remaining <= 0:
            return

        self.remaining -= 1
        if self.remaining == 0:
            if self.then_callback is not None:
                self.repeat_callback = None
                self.then_callback()
            return

    def render(self):
        if self.remaining > 0 and self.repeat_callback is not None:
            self.repeat_callback()
