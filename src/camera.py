from math import sqrt


class Camera:

    def __init__(self, parallax=0.1):
        self.scroll = 0
        self.parallax = parallax

    def to_screen(self, vec, layer=0):
        x, y = vec

        x -= self.scroll * (1 + layer * self.parallax)
        # if layer:
        #     x /= self.parallax * layer

        return (x, y)

    def logic(self, game):
        self.scroll += 1
        screen_pos = self.to_screen(game.player.pos)

        if screen_pos[0] > 100 and game.player.vel.x > 1:
            prop_into_scroll_zone = ((screen_pos[0] - 100) / 300) ** 2
            self.scroll += (screen_pos[0] - 100) * prop_into_scroll_zone
