"""키보드로 Sonic 스프라이트 애니메이션을 확인하는 뷰어."""

from pathlib import Path

try:
    from pico2d import *
except ImportError as error:
    raise SystemExit("Pico2D 라이브러리를 설치한 Python 환경에서 실행하세요.") from error

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 600
TARGET_FPS = 60
ASSET_PATH = Path(__file__).resolve().with_name("sonic-sprite.png")

running = True


def load_sprite_sheet():
    """스크립트와 같은 폴더의 스프라이트 시트를 읽는다."""
    if not ASSET_PATH.is_file():
        raise FileNotFoundError(f"스프라이트 이미지를 찾을 수 없습니다: {ASSET_PATH}")

    try:
        image = load_image(str(ASSET_PATH))
    except Exception as error:
        raise RuntimeError(f"스프라이트 이미지 로드 실패: {ASSET_PATH}") from error

    if image is None:
        raise RuntimeError(f"Pico2D가 스프라이트 이미지를 열지 못했습니다: {ASSET_PATH}")
    return image


def handle_events():
    """창 닫기와 Esc 종료 입력을 처리한다."""
    global running

    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def main():
    global running
    canvas_open = False
    try:
        open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
        canvas_open = True
        sprite_sheet = load_sprite_sheet()
        running = True
        while running:
            handle_events()
            clear_canvas()
            update_canvas()
            delay(1.0 / TARGET_FPS)
    finally:
        if canvas_open:
            close_canvas()


if __name__ == "__main__":
    main()
