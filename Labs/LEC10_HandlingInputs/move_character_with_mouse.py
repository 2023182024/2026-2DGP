from pico2d import *


# fill here
TUK_WIDTH, TUK_HEIGHT=1280,1024
open_canvas(TUK_WIDTH,TUK_HEIGHT)
tuk_ground=load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')


def handle_events():
    global running
    global x,y
    # fill here

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        # fill here
        elif event.type==SDL_MOUSEMOTION:
            x,y=event.x, TUK_HEIGHT-1-events.y
        elif event.type==SDL_KEYDOWN and event.key==SDLK_ESCAPE:
            running=False

running = True
frame = 0
x,y=TUK_WIDTH,TUK_HEIGHT
hide_cursor()
# fill here



while running:
    clear_canvas()

    # fill here
    tuk_ground.draw(TUK_WIDTH//2,TUK_HEIGHT//2)
    character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)

    update_canvas()
    handle_events()
    frame = (frame + 1) % 8
    delay(0.05)

close_canvas()




