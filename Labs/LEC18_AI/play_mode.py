from pico2d import *
import game_world
import game_framework
import common
from ground import Ground
from boy import Boy
from ball import Ball
from zombie import Zombie


def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            common.boy.handle_event(event)


def init():
    ground = Ground()
    game_world.add_oject(ground, 0)

    # 운동장에 흩어져 있는 공 30개 (소년과 좀비가 주울 수 있다)
    # 소년/좀비보다 먼저 추가해서 그들 아래에 그려지도록 한다.
    balls = [Ball() for _ in range(30)]
    game_world.add_objects(balls)

    common.boy = Boy()
    game_world.add_oject(common.boy)

    zombie = Zombie(300, 300)
    game_world.add_oject(zombie)

    game_world.add_collision_pair('boy:ball', common.boy, None)
    game_world.add_collision_pair('zombie:ball', zombie, None)
    for ball in balls:
        game_world.add_collision_pair('boy:ball', None, ball)
        game_world.add_collision_pair('zombie:ball', None, ball)


def pause():
    common.boy.pause()


def resume():
    pass


def finish():
    game_world.clear()
    common.boy = None


def update():
    game_world.update()
    game_world.handle_collisions()  # 모든 객체를 움직인 다음 충돌을 검사한다.


def render():
    clear_canvas()
    game_world.render()
    update_canvas()
