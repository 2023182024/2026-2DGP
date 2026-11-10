from pico2d import get_canvas_width, load_image

import game_world


class Ball:
    images = {}

    def __init__(self, x, y, velocity, ball_type=1):
        if ball_type not in Ball.images:
            image_name = 'ball21x21.png' if ball_type == 1 else 'ball41x41.png'
            Ball.images[ball_type] = load_image(image_name)
        self.x, self.y = x, y
        self.velocity = velocity
        self.image = Ball.images[ball_type]

    def update(self):
        self.x += self.velocity
        if self.x < 0 or self.x > get_canvas_width():
            game_world.remove_object(self)

    def draw(self):
        self.image.draw(self.x, self.y)
