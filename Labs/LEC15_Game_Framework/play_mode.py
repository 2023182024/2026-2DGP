from pico2d import *
import game_world
import game_framework
from boy import Boy
from grass import Grass


paused = False
pause_font = None
inventory_open = False
inventory_image = None


def handle_events():
    global paused, inventory_open

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            paused = not paused
            if paused:
                boy.pause()
            else:
                boy.resume()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            inventory_open = not inventory_open
        elif inventory_open and event.type == SDL_KEYDOWN and event.key == SDLK_0:
            boy.equip_ball(0)
        elif inventory_open and event.type == SDL_KEYDOWN and event.key == SDLK_1:
            boy.equip_ball(1)
        elif inventory_open and event.type == SDL_KEYDOWN and event.key == SDLK_2:
            boy.equip_ball(2)
        elif paused:
            continue
        else:
            boy.handle_event(event)



def init():
    global boy, paused, pause_font, inventory_open, inventory_image

    paused = False
    inventory_open = False
    pause_font = load_font('C:/Windows/Fonts/arial.ttf', 36)
    inventory_image = load_image('item_select.png')

    boy = Boy()
    game_world.add_oject(boy)

    grass = Grass()
    game_world.add_oject(grass, 0)



def update():
    if not paused:
        game_world.update()


def render():
    clear_canvas()
    game_world.render()
    if paused:
        draw_rectangle(250, 250, 550, 350)
        pause_font.draw(310, 285, 'PAUSED', (255, 255, 255))
    if inventory_open:
        inventory_image.draw(400, 300)
    update_canvas()

def finish():
    pass

running = True

