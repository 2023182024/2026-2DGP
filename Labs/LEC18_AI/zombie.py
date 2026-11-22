import random
import math

from pico2d import load_image, load_font, draw_rectangle, get_canvas_width, get_canvas_height

import game_framework
import game_world

# 좀비 달리기 속력: km/h -> 픽셀/초
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# 좀비 애니메이션 속도: 0.5초에 10프레임
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10

ANIMATION_NAMES = ['Walk', 'Idle']


class Zombie:
    images = None
    font = None
    marker_image = None

    def load_images(self):
        if Zombie.images is None:
            Zombie.images = {
                name: [load_image(f'./zombie/{name} ({i}).png') for i in range(1, 11)]
                for name in ANIMATION_NAMES
            }
            Zombie.font = load_font('ENCR10B.TTF', 40)
            Zombie.marker_image = load_image('hand_arrow.png')

    def __init__(self, x=None, y=None):
        self.load_images()
        self.x = x if x is not None else random.randint(100, get_canvas_width() - 100)
        self.y = y if y is not None else random.randint(100, get_canvas_height() - 100)
        self.dir = 0.0  # 이동 방향 (라디안)
        self.speed = 0.0
        self.frame = random.randint(0, 9)
        self.state = 'Idle'
        self.ball_count = 0  # 주운 공의 개수

        self.tx, self.ty = 1000, 1000  # 목표 위치

    def update(self):
        dt = game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt) % FRAMES_PER_ACTION
        # 여기를 채우시오.

    def draw(self):
        image = Zombie.images[self.state][int(self.frame)]
        if math.cos(self.dir) < 0:  # 왼쪽을 향하고 있으면 좌우 반전
            image.composite_draw(0, 'h', self.x, self.y, 100, 100)
        else:
            image.draw(self.x, self.y, 100, 100)
        Zombie.font.draw(self.x - 10, self.y + 60, f'{self.ball_count}', (0, 0, 255))
        Zombie.marker_image.draw(self.tx + 25, self.ty - 25)  # 목표 위치 표시
        draw_rectangle(*self.get_bb())

    # 바운딩 박스: (left, bottom, right, top)
    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def handle_collision(self, group, other):
        if group == 'zombie:ball':
            self.ball_count += 1
