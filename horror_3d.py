from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()
window.title = '3D Horror - Slender Edition'
window.color = color.black

try:
    scene.fog_density = 0.06
    scene.fog_color = color.black
except Exception:
    pass

# Земля
ground = Entity(model='plane', collider='box', scale=150, color=color.dark_gray)

# Игрок
player = FirstPersonController(y=2, origin_y=-.5)
player.cursor.color = color.white
player.speed = 5

WALK_SPEED = 5
SPRINT_SPEED = 9
stamina = 100

# Интерфейс
stamina_bar = Entity(
    parent=camera.ui,
    model='quad',
    color=color.yellow,
    scale=(0.4, 0.02),
    position=(0, -0.45)
)
notes_ui = Text(text="Записки: 0/3", position=(-0.85, 0.45), scale=2, color=color.white)
info_text = Text(
    text="Найди 3 БЕЛЫЕ записки, чтобы открыть выход!\nЖми SHIFT для бега.",
    origin=(0, 0),
    y=0.3,
    scale=1.5,
    color=color.white
)
invoke(destroy, info_text, delay=6)
game_over_text = Text(text="", origin=(0, 0), scale=3, color=color.red, enabled=False)

# Генерация лабиринта
for i in range(70):
    x_pos = random.randint(-40, 40)
    z_pos = random.randint(-40, 40)
    if abs(x_pos) < 5 and abs(z_pos) < 5:
        continue
    Entity(
        model='cube',
        collider='box',
        position=(x_pos, 2, z_pos),
        scale=(random.randint(2, 12), 10, random.randint(2, 12)),
        color=color.dark_gray
    )

# Записки
notes_total = 3
notes_collected = 0
notes = []
for i in range(notes_total):
    nx = random.randint(-40, 40)
    nz = random.randint(-40, 40)
    note = Entity(
        model='cube',
        collider='box',
        position=(nx, 1.5, nz),
        scale=(0.6, 0.6, 0.6),
        color=color.white
    )
    notes.append(note)

# Выход (спрятан под землёй до сбора всех записок)
exit_x = random.choice([-45, 45])
exit_z = random.choice([-45, 45])
exit_zone = Entity(
    model='cube',
    collider='box',
    position=(exit_x, -20, exit_z),
    scale=(2, 10, 2),
    color=color.green
)

# Монстр
monster = Entity(
    model='cube',
    collider='box',
    position=(0, 2, -60),
    scale=(2, 4, 2),
    color=color.red
)

game_finished = False


def update():
    global notes_collected, stamina, game_finished

    if game_finished:
        return

    # Выносливость и спринт
    is_moving = held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']
    if held_keys['shift'] and stamina > 0 and is_moving:
        player.speed = SPRINT_SPEED
        stamina -= time.dt * 25
    else:
        player.speed = WALK_SPEED
        if stamina < 100:
            stamina += time.dt * 15
    stamina = clamp(stamina, 0, 100)

    stamina_bar.scale_x = (stamina / 100) * 0.4
    stamina_bar.color = color.yellow if stamina > 30 else color.red

    # Монстр смотрит на игрока только по горизонтали
    monster_speed = 3.5 + (notes_collected * 0.8)
    monster.look_at(Vec3(player.x, monster.y, player.z))
    monster.position += monster.forward * time.dt * monster_speed

    # Сбор записок
    for note in notes[:]:
        note.rotation_y += time.dt * 100
        if distance(player.position, note.position) < 2.5:
            notes.remove(note)
            destroy(note)
            notes_collected += 1
            notes_ui.text = f"Записки: {notes_collected}/{notes_total}"

            if notes_collected == notes_total:
                notes_ui.text = "ВЫХОД ОТКРЫТ! Ищи зеленое свечение!"
                notes_ui.color = color.green
                exit_zone.y = 2

    # Поражение
    if distance(player.position, monster.position) < 2.5:
        game_finished = True
        game_over_text.text = "ВЫ ПОГИБЛИ\nОно настигло вас."
        game_over_text.color = color.red
        game_over_text.enabled = True
        player.disable()
        return

    # Победа
    if notes_collected == notes_total and distance(player.position, exit_zone.position) < 3.5:
        game_finished = True
        game_over_text.text = "ВЫ СПАСЛИСЬ!"
        game_over_text.color = color.green
        game_over_text.enabled = True
        player.disable()


app.run()
