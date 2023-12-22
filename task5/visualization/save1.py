import tkinter as tk
import os  # Импорт для воспроизведения звука в Unix-подобных системах

# Инициализация основных переменных
water_level = 0
orange_light_on = False
red_light_on = False
siren_on = False
max_water_level = 5  # Максимальный уровень воды для визуализации
canvas_height = 600  # Высота канваса
canvas_width = 600   # Ширина канваса
water_rectangle = None
orange_light_circle = None
red_light_circle = None
siren_symbol = None
sensor_size = 10  # Размер датчика

def play_siren_sound():
    # Воспроизведение стандартного звука системы (замените на свой путь к файлу звука)
    os.system('afplay /System/Library/Sounds/Glass.aiff')

# Функция обновления статуса системы
def update_status():
    global water_level, orange_light_on, red_light_on, siren_on, water_rectangle

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

# Функции управления уровнем воды
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

# Добавление датчиков на уровне 1м
sensor_1_1m = canvas.create_rectangle(30 - sensor_size / 2, canvas_height * 0.8 - sensor_size / 2,
                                   30 + sensor_size / 2, canvas_height * 0.8 + sensor_size / 2, fill="gray")
sensor_2_1m = canvas.create_rectangle(canvas_width / 2 - sensor_size / 2, canvas_height * 0.8 - sensor_size / 2,
                                   canvas_width / 2 + sensor_size / 2, canvas_height * 0.8 + sensor_size / 2, fill="gray")
sensor_3_1m = canvas.create_rectangle(canvas_width - 30 - sensor_size / 2, canvas_height * 0.8 - sensor_size / 2,
                                   canvas_width - 30 + sensor_size / 2, canvas_height * 0.8 + sensor_size / 2, fill="gray")

# Добавление датчиков на уровне 3м
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

# Инициализация интерфейса
update_status()
root.mainloop()
