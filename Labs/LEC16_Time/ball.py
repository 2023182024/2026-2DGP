from pico2d import get_canvas_width, load_image
import game_framework
import game_world

LAUNCH_SPEED_X=50.0
LAUNCH_SPEED_Y=50.0
GRAVITY=9.8 * (10.0/0.3)
GROUND_Y=40

class Ball:
    images = {}

    def __init__(self, x, y, direction, ball_type=1):
        if ball_type not in Ball.images:
            Ball.images[ball_type] = load_image(
                'ball21x21.png' if ball_type == 1 else 'ball41x41.png')
        self.image = Ball.images[ball_type]
        self.x, self.y = x, y
        self.velocity_x = direction * LAUNCH_SPEED_X
        self.velocity_y = LAUNCH_SPEED_Y
        self.radius = 10.5 if ball_type == 1 else 20.5

    def update(self):
        dt = game_framework.frame_time
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt- 0.5 * GRAVITY * dt ** 2
        self.velocity_y-= GRAVITY * dt
        if (self.x <-self.radius or self.x > get_canvas_width() + self.radius
        or self.y- self.radius <= GROUND_Y):
            game_world.remove_object(self)

    def draw(self):
        self.image.draw(self.x, self.y)

