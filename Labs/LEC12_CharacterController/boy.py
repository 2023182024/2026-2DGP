from pico2d import *
from transitions import Machine
import time

class Boy:
    states = ['IDLE', 'WALK', 'RUN', 'SLEEP']

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.image = load_image('animation_sheet.png')
        self.right_pressed = False
        self.left_pressed = False
        self.shift_keys_pressed = set()
        self.last_control_time = time.monotonic()

        self.cursor=300
        state_transitions = [
            {'trigger': 'start_walk', 'source': ['IDLE', 'RUN'], 'dest': 'WALK'},
            {'trigger': 'start_run', 'source': ['IDLE', 'WALK'], 'dest': 'RUN'},
            {'trigger': 'stop_moving', 'source': ['WALK', 'RUN'], 'dest': 'IDLE'},
            {'trigger': 'fall_asleep', 'source': 'IDLE', 'dest': 'SLEEP'},
            {'trigger': 'wake_up', 'source': 'SLEEP', 'dest': 'IDLE'},
        ]
        self.machine = Machine(
            model=self,
            states=Boy.states,
            transitions=state_transitions,
            initial='IDLE',
            auto_transitions=False,
        )

    def handle_keydown(self, key):
        self.last_control_time = time.monotonic()
        if key == SDLK_RIGHT:
            self.face_dir=1
            self.right_pressed = True
        elif key==SDLK_LEFT:
            self.face_dir=2
            self.left_pressed=True
        elif key in (SDLK_LSHIFT, SDLK_RSHIFT):
            self.shift_keys_pressed.add(key)
        self._sync_state_with_input()

    def handle_keyup(self, key):
        self.last_control_time = time.monotonic()
        if key == SDLK_RIGHT:
            self.right_pressed = False
        if key == SDLK_LEFT:
            self.left_pressed = False
        elif key in (SDLK_LSHIFT, SDLK_RSHIFT):
            self.shift_keys_pressed.discard(key)
        self._sync_state_with_input()

    def _sync_state_with_input(self):
        if self.state == 'SLEEP':
            self.wake_up()

        if (self.right_pressed or self.left_pressed) and self.shift_keys_pressed:
            if self.state != 'RUN':
                self.start_run()
        elif self.right_pressed or self.left_pressed:
            if self.state != 'WALK':
                self.start_walk()
        elif self.state in ('WALK', 'RUN'):
            self.stop_moving()

    def update(self):
        if(self.x>20 or self.x<780):
            if self.state == 'WALK':
                if self.face_dir==2:
                    self.x-=5
                else:
                    self.x += 5
            elif self.state == 'RUN':
                if self.face_dir==2:
                    self.x-=15
                else:    
                    self.x += 15


        self.frame = (self.frame + 1) % 8
        if self.state == 'IDLE' and time.monotonic() - self.last_control_time >= 60:
            self.fall_asleep()

    def draw(self):
        
        if self.state=='RUN' or self.state == 'WALK':
            if self.face_dir == 2:
                self.cursor=0
            else:
                self.cursor=100

        else:
            if self.face_dir == 2:
                self.cursor=200
            else:
                self.cursor=300

        if self.state=='SLEEP':
            self.image.clip_composite_draw(self.frame * 100,self.cursor, 100, 100,math.radians(90),'', self.x, self.y-20,100,100)
        else:
            self.image.clip_draw(self.frame * 100,self.cursor, 100, 100, self.x, self.y)