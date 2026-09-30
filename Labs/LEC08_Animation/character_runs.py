from pico2d import *

open_canvas()



grass = load_image('grass.png')
character = load_image('animation_sheet.png')

# fill here
frame=0

while True:

    for index in range(0,400,100):
        for frame in range(0,8):
            clear_canvas()
            grass.draw(400,30)
            character.clip_draw(
                frame*100,index,
                100,100,
                400,90
            )
            update_canvas()
            delay(0.5)

close_canvas()

