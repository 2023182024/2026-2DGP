import random

from pico2d import load_image, draw_rectangle, get_canvas_width, get_canvas_height

import game_world


class Ball:
    image = None

    def __init__(self, x=None, y=None):
        if Ball.image is None:
            Ball.image = load_image('ball21x21.png')
        # 위치를 주지 않으면 운동장 위 임의의 위치에 놓는다.
        self.x = x if x is not None else random.randint(100, get_canvas_width() - 100)
        self.y = y if y is not None else random.randint(100, get_canvas_height() - 100)
        self.radius = 10.5

    def update(self):
        pass  # 바닥에 놓여 있는 공은 움직이지 않는다.

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    # 바운딩 박스: (left, bottom, right, top)
    def get_bb(self):
        r = self.radius
        return self.x - r, self.y - r, self.x + r, self.y + r

    def handle_collision(self, group, other):
        match group:
            case 'boy:ball':
                game_world.remove_object(self)  # 소년이 공을 줍는다.
            case 'zombie:ball':
                game_world.remove_object(self)  # 좀비가 공을 줍는다.
