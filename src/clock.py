from time import time


class Clock:
    def __init__(self, fps):
        self.fps = fps
        self.delay = 1 / fps
        self.last_tick = time()
        self.time_accu = 0

    def __repr__(self):
        return f"<Clock(fps={self.fps}, accu={self.time_accu})>"

    @property
    def time_left(self):
        """Time remaining before the next tick."""
        return max(0, self.delay - self.time_accu)

    @property
    def tick_prop(self):
        """The proportion of time into the next tick."""
        return (1 - self.time_left / self.delay)

    def tick(self):
        """Whether one tick has passed. Consume only one tick if one elapsed."""

        now = time()
        self.time_accu += now - self.last_tick
        self.last_tick = now

        if self.time_accu > self.delay:
            self.time_accu -= self.delay
            return True
        return False

    def tick_all(self):
        """Whether at least one tick has passed. Consumes all the ticks."""
        any_tick = False
        while self.tick():
            any_tick = True

        return any_tick