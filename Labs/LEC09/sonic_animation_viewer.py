"""키보드로 Sonic 스프라이트 애니메이션을 확인하는 뷰어."""

from dataclasses import dataclass
from pathlib import Path
import time

try:
    from pico2d import *
except ImportError as error:
    raise SystemExit("Pico2D 라이브러리를 설치한 Python 환경에서 실행하세요.") from error

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 600
TARGET_FPS = 60
MAX_FRAME_DELTA = 0.1
ASSET_PATH = Path(__file__).resolve().with_name("sonic-sprite.png")
SHEET_WIDTH = 399
SHEET_HEIGHT = 525

SPRITE_SCALE = 8.0
GROUND_Y = 80.0
WALK_SPEED = 180.0
RUN_SPEED = 360.0
ROLL_SPEED = 420.0
ROLL_HOLD_SECONDS = 1.0
JUMP_DURATION = 0.72
JUMP_HEIGHT = 150.0
FRAME_INTERVALS = {
    "idle": 0.16,
    "walk": 0.08,
    "run": 0.06,
    "roll_start": 0.07,
    "roll": 0.07,
    "brake": 0.05,
    "jump": 0.08,
}


@dataclass(frozen=True)
class FrameRect:
    """PNG 왼쪽 위 원점을 기준으로 한 프레임 사각형."""

    x: int
    y: int
    width: int
    height: int

    def pico2d_y(self, sheet_height=SHEET_HEIGHT):
        return sheet_height - self.y - self.height


FRAME_SEQUENCES = {
    "idle": (
        FrameRect(1, 39, 29, 39), FrameRect(31, 40, 26, 38),
        FrameRect(58, 39, 28, 39), FrameRect(86, 40, 30, 38),
        FrameRect(118, 40, 30, 38), FrameRect(150, 40, 30, 38),
        FrameRect(182, 40, 29, 38),
    ),
    "walk": (
        FrameRect(8, 80, 26, 37), FrameRect(37, 80, 27, 37),
        FrameRect(65, 80, 31, 38), FrameRect(97, 80, 37, 37),
        FrameRect(135, 80, 32, 35), FrameRect(170, 79, 32, 38),
        FrameRect(206, 79, 26, 38), FrameRect(238, 80, 24, 37),
        FrameRect(263, 80, 30, 37), FrameRect(295, 80, 36, 37),
        FrameRect(334, 80, 32, 36), FrameRect(370, 79, 29, 38),
    ),
    "run": (
        FrameRect(1, 124, 33, 40), FrameRect(39, 124, 35, 39),
        FrameRect(89, 125, 35, 38), FrameRect(130, 121, 34, 42),
        FrameRect(181, 122, 34, 41), FrameRect(228, 122, 33, 40),
    ),
    "roll_start": (
        FrameRect(1, 169, 29, 30), FrameRect(35, 167, 29, 31),
        FrameRect(67, 169, 30, 29), FrameRect(98, 169, 31, 29),
        FrameRect(131, 168, 29, 30), FrameRect(162, 168, 29, 31),
        FrameRect(193, 170, 30, 29), FrameRect(230, 170, 31, 29),
        FrameRect(268, 170, 30, 30),
    ),
    "roll": (
        FrameRect(1, 206, 30, 27), FrameRect(36, 206, 29, 27),
        FrameRect(70, 206, 29, 27), FrameRect(105, 206, 29, 27),
        FrameRect(139, 206, 29, 27), FrameRect(174, 206, 29, 27),
    ),
}
FRAME_SEQUENCES["jump"] = FRAME_SEQUENCES["roll"]

class AnimationPlayer:
    """동작 프레임을 지정한 시간 간격으로 순환 또는 일회 재생한다."""

    def __init__(self, frames, frame_interval, loop=True):
        if not frames:
            raise ValueError("애니메이션 프레임은 한 개 이상이어야 합니다.")
        if frame_interval <= 0:
            raise ValueError("프레임 간격은 0보다 커야 합니다.")
        self.frames = tuple(frames)
        self.frame_interval = frame_interval
        self.loop = loop
        self.index = 0
        self.elapsed = 0.0
        self.finished = False

    @property
    def frame(self):
        return self.frames[self.index]

    def update(self, delta_time):
        if self.finished:
            return
        self.elapsed += max(0.0, delta_time)
        while self.elapsed >= self.frame_interval:
            self.elapsed -= self.frame_interval
            if self.index + 1 < len(self.frames):
                self.index += 1
            elif self.loop:
                self.index = 0
            else:
                self.elapsed = 0.0
                self.finished = True
                return

running = True
held_keys = set()
horizontal_key_order = []
pressed_direction_keys = []
jump_pressed = False


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


def draw_frame(image, frame, x, vertical_offset=0.0, facing_left=False):
    """프레임을 확대하고 발 기준선에 맞춰 그린다."""
    draw_width = frame.width * SPRITE_SCALE
    if facing_left:
        draw_width = -draw_width
    draw_height = frame.height * SPRITE_SCALE
    draw_y = GROUND_Y + vertical_offset + draw_height / 2
    image.clip_draw(
        frame.x,
        frame.pico2d_y(),
        frame.width,
        frame.height,
        x,
        draw_y,
        draw_width,
        draw_height,
    )



def clamp_view_position(x, vertical_offset, frame):
    """확대된 프레임 경계가 창 바깥으로 나가지 않도록 위치를 제한한다."""
    draw_width = frame.width * SPRITE_SCALE
    draw_height = frame.height * SPRITE_SCALE
    half_width = draw_width / 2
    x = min(max(x, half_width), CANVAS_WIDTH - half_width)
    max_vertical_offset = max(0.0, CANVAS_HEIGHT - GROUND_Y - draw_height)
    vertical_offset = min(max(vertical_offset, 0.0), max_vertical_offset)
    return x, vertical_offset

def handle_events():
    """종료, 방향키, Shift와 점프 입력의 눌림 상태를 추적한다."""
    global running, jump_pressed
    pressed_direction_keys.clear()
    jump_pressed = False

    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key in (
                SDLK_LEFT, SDLK_RIGHT, SDLK_LSHIFT, SDLK_RSHIFT, SDLK_SPACE
            ) and event.key not in held_keys:
                held_keys.add(event.key)
                if event.key in (SDLK_LEFT, SDLK_RIGHT):
                    horizontal_key_order.append(event.key)
                    pressed_direction_keys.append(event.key)
                elif event.key == SDLK_SPACE:
                    jump_pressed = True
        elif event.type == SDL_KEYUP:
            held_keys.discard(event.key)
            if event.key in horizontal_key_order:
                horizontal_key_order.remove(event.key)



def print_controls():
    """콘솔에 창 크기와 키 조작 방법을 한 번 안내한다."""
    print("Sonic 애니메이션 뷰어 (1200 x 600)")
    print("방향키: 걷기 | 방향키 + Shift: 달리기")
    print("방향키 + Shift 1초 유지: 구르기 | Space: 점프 | Esc: 종료")

def current_direction():
    """동시에 누른 방향키 중 마지막으로 누른 방향을 반환한다."""
    if not horizontal_key_order:
        return 0
    return -1 if horizontal_key_order[-1] == SDLK_LEFT else 1


def shift_is_held():
    return SDLK_LSHIFT in held_keys or SDLK_RSHIFT in held_keys

def main():
    global running
    canvas_open = False
    try:
        open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
        canvas_open = True
        sprite_sheet = load_sprite_sheet()
        print_controls()
        players = {
            "idle": AnimationPlayer(
                FRAME_SEQUENCES["idle"], FRAME_INTERVALS["idle"], loop=True
            ),
            "walk": AnimationPlayer(
                FRAME_SEQUENCES["walk"], FRAME_INTERVALS["walk"], loop=True
            ),
            "run": AnimationPlayer(
                FRAME_SEQUENCES["run"], FRAME_INTERVALS["run"], loop=True
            ),
            "roll_start": AnimationPlayer(
                FRAME_SEQUENCES["roll_start"],
                FRAME_INTERVALS["roll_start"],
                loop=False,
            ),
            "roll": AnimationPlayer(
                FRAME_SEQUENCES["roll"], FRAME_INTERVALS["roll"], loop=True
            ),
            "brake": AnimationPlayer(
                tuple(reversed(FRAME_SEQUENCES["run"]))
                + FRAME_SEQUENCES["run"][:3],
                FRAME_INTERVALS["brake"],
                loop=False,
            ),
            "jump": AnimationPlayer(
                FRAME_SEQUENCES["jump"], FRAME_INTERVALS["jump"], loop=True
            ),
        }
        mode = "idle"
        held_keys.clear()
        horizontal_key_order.clear()
        pressed_direction_keys.clear()
        run_held_time = 0.0
        run_direction = 0
        jump_elapsed = 0.0
        jump_offset = 0.0
        brake_old_direction = 0
        brake_target_direction = 0
        x = CANVAS_WIDTH / 2
        facing_left = False
        running = True

        def enter_mode(next_mode):
            nonlocal mode
            if mode != next_mode:
                mode = next_mode
                players[mode].reset()
            return players[mode]

        previous_time = time.perf_counter()
        while running:
            current_time = time.perf_counter()
            delta_time = min(MAX_FRAME_DELTA, max(0.0, current_time - previous_time))
            previous_time = current_time
            handle_events()
            direction = current_direction()
            if direction:
                facing_left = direction < 0
            shift_down = shift_is_held()
            jump_offset = 0.0

            if jump_pressed and mode != "jump":
                enter_mode("jump")
                jump_elapsed = 0.0

            if mode == "jump":
                if direction and shift_down:
                    if run_direction != direction:
                        run_held_time = 0.0
                        run_direction = direction
                    run_held_time += delta_time
                else:
                    run_held_time = 0.0
                    run_direction = 0
                jump_elapsed = min(JUMP_DURATION, jump_elapsed + delta_time)
                jump_progress = jump_elapsed / JUMP_DURATION
                jump_offset = 4 * JUMP_HEIGHT * jump_progress * (1 - jump_progress)
                if direction:
                    air_speed = RUN_SPEED if shift_down else WALK_SPEED
                    x += direction * air_speed * delta_time
                current_player = players["jump"]
                current_player.update(delta_time)
                if jump_elapsed >= JUMP_DURATION:
                    jump_offset = 0.0
                    mode = "jump_done"
            else:
                reverse_pressed = any(
                    (key == SDLK_LEFT and direction == -1)
                    or (key == SDLK_RIGHT and direction == 1)
                    for key in pressed_direction_keys
                )
                if (
                    mode == "run"
                    and shift_down
                    and direction == -run_direction
                    and reverse_pressed
                ):
                    brake_old_direction = run_direction
                    brake_target_direction = direction
                    run_held_time = 0.0
                    enter_mode("brake")
                if mode == "brake":
                    current_player = players["brake"]
                    current_player.update(delta_time)
                    if current_player.index < len(FRAME_SEQUENCES["run"]):
                        facing_left = brake_old_direction < 0
                    else:
                        facing_left = brake_target_direction < 0
                    if current_player.finished:
                        enter_mode("run")
                        run_direction = brake_target_direction
                        run_held_time = 0.0
                elif direction and shift_down:
                    if run_direction != direction:
                        run_held_time = 0.0
                        run_direction = direction
                        enter_mode("run")
                    if mode not in ("roll_start", "roll"):
                        run_held_time += delta_time
                        if run_held_time >= ROLL_HOLD_SECONDS:
                            enter_mode("roll_start")
                    if mode == "roll_start":
                        current_player = players["roll_start"]
                        current_player.update(delta_time)
                        x += direction * ROLL_SPEED * delta_time
                        if current_player.finished:
                            enter_mode("roll")
                    elif mode == "roll":
                        current_player = players["roll"]
                        current_player.update(delta_time)
                        x += direction * ROLL_SPEED * delta_time
                    else:
                        current_player = enter_mode("run")
                        current_player.update(delta_time)
                        x += direction * RUN_SPEED * delta_time
                else:
                    run_held_time = 0.0
                    run_direction = 0
                    if direction:
                        current_player = enter_mode("walk")
                        current_player.update(delta_time)
                        x += direction * WALK_SPEED * delta_time
                    else:
                        current_player = enter_mode("idle")
                        current_player.update(delta_time)

            x, jump_offset = clamp_view_position(x, jump_offset, current_player.frame)
            clear_canvas()
            draw_frame(
                sprite_sheet,
                current_player.frame,
                x,
                vertical_offset=jump_offset,
                facing_left=facing_left,
            )
            update_canvas()
            delay(1.0 / TARGET_FPS)
    finally:
        if canvas_open:
            close_canvas()

if __name__ == "__main__":
    main()
