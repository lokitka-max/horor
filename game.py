import time
import sys
import os
import random

def slow_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause(seconds=1.5):
    time.sleep(seconds)

def ask(prompt, choices):
    while True:
        slow_print(f"\n{prompt}")
        for i, c in enumerate(choices, 1):
            print(f"  [{i}] {c}")
        ans = input("\n> ").strip()
        if ans.isdigit() and 1 <= int(ans) <= len(choices):
            return int(ans)
        slow_print("Введи число из списка.")

# ─────────────────────────────────────────────
# Концовки
# ─────────────────────────────────────────────

def ending_escape():
    clear()
    slow_print("\n" + "="*50)
    slow_print("  КОНЕЦ: ТЫ ВЫЖИЛ")
    slow_print("="*50)
    slow_print("\nТы выбегаешь из дома. Холодный ночной воздух")
    slow_print("обжигает лёгкие. Позади — тишина.")
    slow_print("\nТы оборачиваешься. В окне второго этажа")
    slow_print("что-то движется.")
    slow_print("\nТы бежишь. И не останавливаешься.")
    slow_print("\n... но иногда тебе снится этот дом.\n")

def ending_dead(reason):
    clear()
    slow_print("\n" + "="*50)
    slow_print("  КОНЕЦ: ТЫ МЁРТВ")
    slow_print("="*50)
    slow_print(f"\n{reason}\n")

def ending_trapped():
    clear()
    slow_print("\n" + "="*50)
    slow_print("  КОНЕЦ: ТЫ ОСТАЛСЯ ЗДЕСЬ НАВСЕГДА")
    slow_print("="*50)
    slow_print("\nДверь больше не открывается.")
    slow_print("Свет гаснет. Ты слышишь шаги — они приближаются.")
    slow_print("\nПотом — ничего.\n")

# ─────────────────────────────────────────────
# Сцены
# ─────────────────────────────────────────────

def scene_basement(inventory):
    clear()
    slow_print("\n[ ПОДВАЛ ]")
    pause()
    slow_print("\nТы спускаешься по скрипучим ступеням.")
    slow_print("В углу — старый стол. На нём лежит фонарик.")
    pause()

    if "фонарик" not in inventory:
        choice = ask("Взять фонарик?", ["Да", "Нет, уходить отсюда"])
        if choice == 1:
            inventory.append("фонарик")
            slow_print("\nФонарик тяжёлый, но рабочий. Батарейки ещё живые.")
            pause()

    slow_print("\nТы замечаешь люк в полу. Он приоткрыт.")
    slow_print("Снизу — абсолютная тьма и запах сырости.")
    pause()

    choice = ask("Что делать?", ["Открыть люк и заглянуть", "Вернуться наверх"])
    if choice == 1:
        if "фонарик" in inventory:
            slow_print("\nТы светишь вниз. Там — узкий тоннель.")
            slow_print("На стенах — царапины. Много царапин. Как от ногтей.")
            pause()
            slow_print("\nЧто-то в темноте МОРГАЕТ.")
            pause(2)
            slow_print("\nТы захлопываешь люк и бежишь наверх.")
        else:
            slow_print("\nТемнота непроглядная. Ты наклоняешься ближе...")
            pause()
            slow_print("\nЧто-то хватает тебя за руку и тянет вниз.")
            pause(2)
            ending_dead("Тьма под домом оказалась живой. Люк закрылся сам собой.")
            return False
    return True

def scene_library(inventory):
    clear()
    slow_print("\n[ БИБЛИОТЕКА ]")
    pause()
    slow_print("\nПолки забиты старыми книгами. Некоторые сожжены.")
    slow_print("На столе — раскрытый дневник.")
    pause()

    choice = ask("Читать дневник?", ["Да", "Не трогать"])
    if choice == 1:
        slow_print("\n--- запись от 14 октября ---")
        slow_print('"Оно возвращается каждую ночь. Не смотри ему в глаза.')
        slow_print('Не зажигай свет. Не произноси его имя."')
        pause()
        slow_print("\nПоследняя строчка написана другим почерком,")
        slow_print('почти нечитаемо: "ОНО ВНУТРИ СТЕН"')
        pause(2)
        inventory.append("знание")
        slow_print('\n[Ты запомнил: не смотреть в глаза.]')

    slow_print("\nВнезапно книга падает с полки сама собой.")
    pause()
    slow_print("Страницы открываются на одной и той же фразе,")
    slow_print('снова и снова: "УХОДИ УХОДИ УХОДИ"')
    pause(2)
    return True

def scene_hallway(inventory):
    clear()
    slow_print("\n[ КОРИДОР ВТОРОГО ЭТАЖА ]")
    pause()
    slow_print("\nДлинный тёмный коридор. В конце — закрытая дверь.")
    slow_print("Из-за неё доносится тихое пение. Детское.")
    pause(2)

    choice = ask("Идти к двери?", [
        "Идти прямо к двери",
        "Двигаться вдоль стены, медленно",
        "Уйти обратно"
    ])

    if choice == 3:
        slow_print("\nТы разворачиваешься. За тобой — кто-то стоит.")
        pause()
        slow_print("Высокий. Неподвижный. Голова наклонена под неестественным углом.")
        pause(2)
        if "знание" in inventory:
            slow_print("\nТы вспоминаешь дневник: не смотреть в глаза.")
            slow_print("Ты смотришь в пол и медленно обходишь фигуру.")
            pause(2)
            slow_print("Она не двигается.")
            return "side"
        else:
            slow_print("\nТы инстинктивно смотришь ему в лицо.")
            pause()
            slow_print("У него нет лица.")
            pause(2)
            ending_dead("Последнее, что ты слышал — детское пение, ставшее криком.")
            return False

    if choice == 1:
        slow_print("\nТы идёшь уверенно. Пение стихает.")
        slow_print("Доходишь до двери и берёшься за ручку.")
        pause()
        slow_print("Дверь открывается сама — внутри никого.")
        slow_print("Только детский стул посреди пустой комнаты.")
        slow_print("И на нём — твоя фотография.")
        pause(2)
        return "door"

    if choice == 2:
        slow_print("\nТы идёшь вдоль стены, касаясь её рукой.")
        slow_print("Под пальцами — выпуклости. Ты подносишь фонарик...")
        if "фонарик" in inventory:
            pause()
            slow_print("\nВ стене — лица. Десятки застывших лиц под штукатуркой.")
            slow_print("Один из них открывает глаза.")
            pause(2)
            slow_print("\nТы бежишь. Стена трескается тебе вслед.")
            return "door"
        else:
            slow_print("...но в темноте ничего не видно.")
            slow_print("Ты продолжаешь идти. Что-то хватает тебя за руку из стены.")
            pause(2)
            ending_dead("Стена поглотила тебя. Теперь ты тоже — часть дома.")
            return False

def scene_exit(inventory, path):
    clear()
    slow_print("\n[ ГЛАВНЫЙ ХОЛЛ — ВЫХОД ]")
    pause()
    slow_print("\nТы видишь входную дверь. Она в десяти метрах.")
    pause()

    if path == "door":
        slow_print("\nПозади тебя — скрип. Медленный. Ритмичный.")
        slow_print("Ты не оборачиваешься.")
        pause(2)
        choice = ask("Что делать?", [
            "Бежать к двери со всех ног",
            "Идти медленно, не издавая звуков"
        ])
        if choice == 1:
            slow_print("\nТы бежишь. Скрип за тобой ускоряется.")
            slow_print("Дверь — заперта. Ты дёргаешь ручку...")
            pause()
            slow_print("Замок поддаётся. Ты вырываешься наружу.")
            pause()
            ending_escape()
        else:
            slow_print("\nТы делаешь шаг. Скрип стихает.")
            slow_print("Ещё шаг. Тишина.")
            slow_print("Три метра до двери. Два. Один.")
            pause()
            slow_print("\nЧто-то касается твоего плеча.")
            pause(2)
            if "знание" in inventory:
                slow_print("\nТы не оборачиваешься. Дневник говорил: не смотри.")
                slow_print("Ты открываешь дверь и шагаешь в ночь.")
                pause()
                ending_escape()
            else:
                slow_print("\nТы оборачиваешься.")
                pause(2)
                ending_trapped()

    else:
        slow_print("\nПуть к двери свободен. Почти.")
        slow_print("Посреди холла стоит детский стул. На нём — твоя фотография.")
        slow_print("Та самая, что ты видел наверху.")
        pause(2)
        choice = ask("Взять фотографию?", ["Взять", "Обойти и бежать к двери"])
        if choice == 2:
            slow_print("\nТы обходишь стул. Фотография поворачивается тебе вслед.")
            pause()
            slow_print("Ты не смотришь. Дверь открывается с первого раза.")
            pause()
            ending_escape()
        else:
            slow_print("\nТы берёшь фотографию.")
            slow_print("На обороте написано: 'Ты должен был уйти раньше.'")
            pause(2)
            slow_print("\nДверь исчезает.")
            pause(2)
            ending_trapped()

# ─────────────────────────────────────────────
# Интро и основной поток
# ─────────────────────────────────────────────

def intro():
    clear()
    slow_print("\n" + "="*50, 0.01)
    slow_print("       З А Б Р О Ш Е Н Н Ы Й   Д О М", 0.05)
    slow_print("="*50, 0.01)
    slow_print("\n  Текстовый хоррор | ~5 минут | 3 концовки")
    slow_print("="*50, 0.01)
    pause(1)
    slow_print("\nТы журналист. Ты пишешь о городских легендах.")
    slow_print("Заброшенный дом на краю города — идеальная история.")
    pause()
    slow_print("\nТвой редактор не верит в паранормальное.")
    slow_print("Ты тоже не верил.")
    pause(2)
    slow_print("\nДверь за тобой захлопывается сама.")
    slow_print("Телефон — без сигнала.")
    pause(2)

def choose_path():
    clear()
    slow_print("\n[ ПЕРВЫЙ ЭТАЖ ]")
    pause()
    slow_print("\nПрихожая. Темно. Пахнет плесенью и чем-то ещё.")
    slow_print("Перед тобой три пути:")
    slow_print("  — дверь в подвал слева")
    slow_print("  — библиотека справа")
    slow_print("  — лестница наверх прямо")
    pause()
    return ask("Куда идти?", [
        "В подвал",
        "В библиотеку",
        "На второй этаж"
    ])

def main():
    intro()
    inventory = []

    choice = choose_path()

    # Первая сцена
    if choice == 1:
        ok = scene_basement(inventory)
        if not ok:
            return
        # После подвала — идём в библиотеку или сразу наверх
        c2 = ask("Ты поднялся в холл. Куда дальше?", [
            "В библиотеку",
            "Сразу на второй этаж"
        ])
        if c2 == 1:
            ok = scene_library(inventory)
            if not ok:
                return

    elif choice == 2:
        ok = scene_library(inventory)
        if not ok:
            return
        c2 = ask("Ты в холле. Куда дальше?", [
            "В подвал",
            "Сразу на второй этаж"
        ])
        if c2 == 1:
            ok = scene_basement(inventory)
            if not ok:
                return

    else:
        # Сразу наверх — без подготовки
        slow_print("\nТы идёшь к лестнице. Под ногой — скрип.")
        slow_print("Где-то внизу что-то упало.")
        pause()
        slow_print("Ты продолжаешь подниматься.")
        pause()

    # Второй этаж
    path = scene_hallway(inventory)
    if not path:
        return

    # Финальная сцена
    scene_exit(inventory, path)

    slow_print("\n" + "-"*50)
    play_again = input("Сыграть снова? (д/н): ").strip().lower()
    if play_again in ("д", "y", "yes", "да"):
        main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[Ты сбежал из игры. Мудрое решение.]\n")
