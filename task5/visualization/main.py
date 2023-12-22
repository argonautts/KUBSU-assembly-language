import tkinter as tk
import os
import time

# Инициализация основных переменных
water_level = 0
old_water_level = water_level
orange_light_on = False
red_light_on = False
siren_on = False
timer_started = False
start_time = None
current_time = 0
current_mA = 15  # начальное значение силы тока
max_water_level = 5  # Максимальный уровень воды для визуализации
canvas_height = 600  # Высота канваса
canvas_width = 600   # Ширина канваса
water_rectangle = None
orange_light_circle = None
red_light_circle = None
siren_symbol = None
sensor_size = 10  # Размер датчика

# Словарь для значений силы тока в зависимости от времени
current_values = {0: 15, 0.5: 16, 1: 17, 1.5: 18.5, 2: 19.5, 2.5: 20, 3: 20.5, 3.5: 20.8, 4: 21, 4.5: 21.2, 5: 21.4,
                  5.5: 21.6, 6: 21.7, 6.5: 21.8, 7: 21.85, 7.5: 21.88, 8: 21.9, 8.5: 21.93, 9: 21.95, 9.5: 21.97, 10: 22}

def play_siren_sound():
    # Воспроизведение стандартного звука системы
    os.system('afplay /System/Library/Sounds/Glass.aiff')

def reset_timer_and_current():
    global timer_started, start_time, current_time, current_mA
    timer_started = False
    start_time = None
    current_time = 0
    current_mA = 15  # Сброс к начальной силе тока

def update_timer_and_current():
    global timer_started, start_time, current_time, current_mA

    if red_light_on and not timer_started:
        start_time = time.time()
        timer_started = True

    if timer_started:
        current_time = time.time() - start_time
        if current_time > 10:
            current_time = 10
            timer_started = True  # Останавливаем таймер после 10 секунд
        current_mA = current_values.get(int(current_time), 22)  # Обновление силы тока

    # Обновляем метки на интерфейсе
    timer_label.config(text=f"Время: {current_time:.1f} сек")
    current_label.config(text=f"Сила тока: {current_mA} мА")

def update_status():
    global water_level, orange_light_on, red_light_on, siren_on, water_rectangle, old_water_level

    if water_level < old_water_level:  # Проверка, уменьшился ли уровень воды
        reset_timer_and_current()

    old_water_level = water_level  # Обновление предыдущего уровня воды

    if water_level >= 1:
        orange_light_on = True
    else:
        orange_light_on = False

    if water_level >= 3:
        red_light_on = True
        siren_on = True
    else:
        red_light_on = False
        siren_on = False

    if siren_on:
        play_siren_sound()

    # Обновление визуализации воды
    water_height = water_level / max_water_level * canvas_height
    canvas.coords(water_rectangle, 10, canvas_height - water_height, canvas_width - 10, canvas_height)

    # Обновление индикаторов ламп и гудка
    canvas.itemconfig(orange_light_circle, fill=("orange" if orange_light_on else "white"))
    canvas.itemconfig(red_light_circle, fill=("red" if red_light_on else "white"))
    canvas.itemconfig(siren_symbol, state=("normal" if siren_on else "hidden"))

    # Обновление метки уровня воды
    water_level_label.config(text=f"Уровень воды: {water_level} м")

def increase_water_level():
    global water_level
    water_level = min(water_level + 0.5, max_water_level)
    update_status()

def decrease_water_level():
    global water_level
    water_level = max(water_level - 0.5, 0)
    update_status()

# Создание интерфейса
root = tk.Tk()
root.title("Контроль за аварийным подъемом воды")

canvas = tk.Canvas(root, height=canvas_height, width=canvas_width)
water_rectangle = canvas.create_rectangle(10, canvas_height, canvas_width - 10, canvas_height, fill="blue")

# Расположение оранжевой и красной лампы, а также гудка
orange_light_circle = canvas.create_oval(20, 20, 60, 60, outline="black", fill="white")
red_light_circle = canvas.create_oval(canvas_width - 60, 20, canvas_width - 20, 60, outline="black", fill="white")
siren_symbol = canvas.create_text(canvas_width / 2, 40, text="🔊", font=("Arial", 24), state="hidden")

# Добавление горизонтальных линий для 1м и 3м уровней
line_1m = canvas.create_line(0, canvas_height * 0.8, canvas_width, canvas_height * 0.8, fill="black")
line_3m = canvas.create_line(0, canvas_height * 0.4, canvas_width, canvas_height * 0.4, fill="black")

# Добавление датчиков на уровне 1м и 3м
sensor_1_1m = canvas.create_rectangle(30 - sensor_size / 2, canvas_height * 0.8 - sensor_size / 2,
                                   30 + sensor_size / 2, canvas_height * 0.8 + sensor_size / 2, fill="gray")
sensor_2_1m = canvas.create_rectangle(canvas_width / 2 - sensor_size / 2, canvas_height * 0.8 - sensor_size / 2,
                                   canvas_width / 2 + sensor_size / 2, canvas_height * 0.8 + sensor_size / 2, fill="gray")
sensor_3_1m = canvas.create_rectangle(canvas_width - 30 - sensor_size / 2, canvas_height * 0.8 - sensor_size / 2,
                                   canvas_width - 30 + sensor_size / 2, canvas_height * 0.8 + sensor_size / 2, fill="gray")

sensor_1_3m = canvas.create_rectangle(30 - sensor_size / 2, canvas_height * 0.4 - sensor_size / 2,
                                   30 + sensor_size / 2, canvas_height * 0.4 + sensor_size / 2, fill="gray")
sensor_2_3m = canvas.create_rectangle(canvas_width / 2 - sensor_size / 2, canvas_height * 0.4 - sensor_size / 2,
                                   canvas_width / 2 + sensor_size / 2, canvas_height * 0.4 + sensor_size / 2, fill="gray")
sensor_3_3m = canvas.create_rectangle(canvas_width - 30 - sensor_size / 2, canvas_height * 0.4 - sensor_size / 2,
                                   canvas_width - 30 + sensor_size / 2, canvas_height * 0.4 + sensor_size / 2, fill="gray")

canvas.pack()

water_level_label = tk.Label(root)
water_level_label.pack()

increase_button = tk.Button(root, text="Увеличить уровень воды", command=increase_water_level)
increase_button.pack()

decrease_button = tk.Button(root, text="Уменьшить уровень воды", command=decrease_water_level)
decrease_button.pack()

# Добавляем метки для отображения времени и силы тока
timer_label = tk.Label(root)
timer_label.pack()

current_label = tk.Label(root)
current_label.pack()

update_status()

# Главный цикл обновления
while True:
    update_timer_and_current()
    root.update_idletasks()
    root.update()
