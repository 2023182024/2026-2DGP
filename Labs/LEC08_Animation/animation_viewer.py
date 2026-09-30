from pico2d import *

open_canvas()

qiqi= load_image('qiqi_sprite(made_by_gemini).png')

frame=0

while True:
    x=159
    for index in range(106,550,87):
        clear_canvas()
        qiqi.clip_draw(
            index,x,
            42,86,
            100,100
        )
        update_canvas()
        delay(0.5)
    pass