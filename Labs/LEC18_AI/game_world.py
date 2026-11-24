world = [[], [], []]  # 0: 배경, 1: 오브젝트, 2: UI

# 충돌 그룹: { 'a:b' : [ [a 그룹 객체들], [b 그룹 객체들] ] }
collision_pairs = {}


def add_oject(o, depth=1):
    world[depth].append(o)


def add_objects(ol, depth=1):
    world[depth] += ol


def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)


def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)  # 월드에서 지우면 충돌 그룹에서도 지운다.
            return


def update():
    for layer in world:
        for o in layer[:]:
            o.update()


def render():
    for layer in world:
        for o in layer[:]:
            o.draw()


def clear():
    for layer in world:
        layer.clear()
    collision_pairs.clear()


# ---------------- 충돌 처리 ----------------

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        print(f'Added new group {group}')
        collision_pairs[group] = [[], []]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)


def remove_collision_pair(group, a, b):
    if group in collision_pairs:
        if a and a in collision_pairs[group][0]:
            collision_pairs[group][0].remove(a)
        if b and b in collision_pairs[group][1]:
            collision_pairs[group][1].remove(b)


def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0][:]:          # 충돌 처리 중 객체가 삭제될 수 있으므로 복사본으로 순회
            for b in pairs[1][:]:
                if a not in pairs[0]:  # a 가 이미 삭제되었으면 중단
                    break
                if b not in pairs[1]:
                    continue
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)
