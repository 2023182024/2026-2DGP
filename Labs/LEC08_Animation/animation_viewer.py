from pico2d import *

open_canvas()

qiqi= load_image('qiqi_sprite(made_by_gemini)_transparent.png')



while True:

    x=522
    for index in range(20,550,86):
        clear_canvas()
        qiqi.clip_draw(
            index,x,
            42,86,
            400,300
        )
        update_canvas()
        delay(1)

    x=402
    for index in range(15,723, 85):
        clear_canvas()
        qiqi.clip_draw(
            index,x,
            50,88,
            400,300
        )
        update_canvas()
        delay(1)

    pass