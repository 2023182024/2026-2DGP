from pico2d import *


open_canvas()
grass = load_image('grass.png')
character = load_image('animation_sheet.png')


def handle_events():
    global running
    global x
    global dir
    # fill here

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type==SDL_KEYDOWN:
            if event.key==SDLK_RIGHT:
                dir+=1
            elif event.key==SDLK_LEFT:
                dir-=1
            elif event.key==SDLK_ESCAPE:
                running=False
        elif event.type==SDL_KEYUP: 
            if event.key==SDLK_RIGHT:
                dir-=1
            elif event.key==SDLK_LEFT:
                dir+=1
        # fill here


running = True
x = 800 // 2
frame = 0
dir=0
# fill here
while running:
    clear_canvas()
    grass.draw(400,30)
    if(dir<0):
        character.clip_composite_draw(frame*100,100,100,100,0,'h',x,90)
    else:
        character.clip_draw(frame*100,100,100,100,x,90)
    update_canvas()
    handle_events()

    frame=(frame+1)%8
    delay(0.05)
    x+=dir*5
    if not running:
        break

close_canvas()

