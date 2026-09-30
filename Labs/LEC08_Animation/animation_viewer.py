from pico2d import *

open_canvas()

qiqi= load_image('qiqi_sprite(made_by_gemini)_transparent.png')



while True:

    print("walking")
    x=522
    for index in range(20,376,86):
        clear_canvas()
        qiqi.clip_draw(
            index,x,
            52,86,
            400,300
        )
        update_canvas()
        delay(1)

    print("running")
    x=402
    for index in range(15,723, 85):
        clear_canvas()
        qiqi.clip_draw(
            index,x,
            70,88,
            400,300
        )
        update_canvas()
        delay(1)

    print("jumping")
    x=33
    for index in range(20,503,120):
        clear_canvas()
        qiqi.clip_draw(
            index,x,
            50,100,
            400,300
        )
        update_canvas()
        delay(1)

    pass