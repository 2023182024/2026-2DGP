from pico2d import get_canvas_width, load_image

import game_world


class Ball:
    SPEED = 10
    HALF_SIZE = 11

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = 1 if direction >= 0 else -1
        self.image = load_image('ball21x21.png')

    def update(self):
        self.x += self.direction * self.SPEED
        if (self.x < -self.HALF_SIZE or
                self.x > get_canvas_width() + self.HALF_SIZE):
            game_world.remove(self)

    def draw(self):
        self.image.draw(self.x, self.y)