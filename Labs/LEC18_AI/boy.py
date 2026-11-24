from pico2d import *

from sdl2 import (SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT,
                  SDLK_UP, SDLK_DOWN)
from transitions import Machine

import game_framework

# 달리기 속력을 시속 km에서 초속 m, 다시 초당 픽셀로 변환한다.
# 좀비(10km/h)에게서 도망칠 수 있도록 소년이 더 빠르다.
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# 애니메이션 속도: 0.5초에 8프레임
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

MOVE_KEYS = (SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN)


class Idle:
    def enter(self, boy):
        boy.frame = 0

    def do(self, boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    def draw(self, boy):
        row = 300 if boy.face_dir == 1 else 200
        boy.image.clip_draw(int(boy.frame) * 100, row, 100, 100, boy.x, boy.y)

    def move(self, boy):
        boy.start_run()


class Run:
    def enter(self, boy):
        boy.frame = 0

    def do(self, boy):
        dt = game_framework.frame_time
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt) % FRAMES_PER_ACTION
        boy.x += boy.xdir * RUN_SPEED_PPS * dt
        boy.y += boy.ydir * RUN_SPEED_PPS * dt
        boy.x = clamp(25, boy.x, get_canvas_width() - 25)
        boy.y = clamp(50, boy.y, get_canvas_height() - 50)

    def draw(self, boy):
        # 위/아래로만 움직일 때는 바라보던 방향을 유지한다.
        row = 100 if boy.face_dir == 1 else 0
        boy.image.clip_draw(int(boy.frame) * 100, row, 100, 100, boy.x, boy.y)

    def move(self, boy):
        pass


class Boy:
    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 16)
        self.x, self.y = 100, 100
        self.frame = 0
        self.image = load_image('animation_sheet.png')
        self.xdir, self.ydir = 0, 0
        self.face_dir = 1
        self.pressed_keys = set()
        self.ball_count = 0  # 주운 공의 개수

        self.states = {'IDLE': Idle(), 'RUN': Run()}

        self.machine = Machine(
            model=self,
            states=['IDLE', 'RUN'],
            transitions=[
                {'trigger': 'start_run',
                 'source': 'IDLE', 'dest': 'RUN'},
                {'trigger': 'stop_run',
                 'source': 'RUN', 'dest': 'IDLE'},
            ],
            initial='IDLE',
            auto_transitions=False,
        )

    def on_enter_IDLE(self):
        self.states['IDLE'].enter(self)

    def on_enter_RUN(self):
        self.states['RUN'].enter(self)

    def pause(self):
        self.pressed_keys.clear()
        self.xdir = self.ydir = 0
        if self.state == 'RUN':
            self.stop_run()

    def handle_event(self, event):
        if event.type not in (SDL_KEYDOWN, SDL_KEYUP) or event.key not in MOVE_KEYS:
            return

        if event.type == SDL_KEYDOWN:
            self.pressed_keys.add(event.key)
        else:
            self.pressed_keys.discard(event.key)

        self.xdir = int(SDLK_RIGHT in self.pressed_keys) - int(SDLK_LEFT in self.pressed_keys)
        self.ydir = int(SDLK_UP in self.pressed_keys) - int(SDLK_DOWN in self.pressed_keys)

        if self.xdir != 0:
            self.face_dir = self.xdir

        if self.xdir != 0 or self.ydir != 0:
            self.states[self.state].move(self)
        elif self.state == 'RUN':
            self.stop_run()

    def update(self):
        self.states[self.state].do(self)

    def draw(self):
        self.states[self.state].draw(self)
        self.font.draw(self.x - 10, self.y + 50, f'{self.ball_count:02d}', (255, 255, 0))
        draw_rectangle(*self.get_bb())

    # 바운딩 박스: (left, bottom, right, top)
    def get_bb(self):
        return self.x - 20, self.y - 50, self.x + 20, self.y + 50

    def handle_collision(self, group, other):
        if group == 'boy:ball':
            self.ball_count += 1
