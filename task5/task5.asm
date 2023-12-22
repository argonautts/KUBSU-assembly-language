section .data
    horn_values dw 180h, 19Ah, 1B3h, 1DAh, 1F3h, 200h, 20Dh, 214h, 21Ah, 21Fh, 224h, 229h, 22Ch, 22Eh, 22Fh, 230h, 231h, 231h, 232h, 232h, 233h.   ; Значения для гудка
    orange_lamp db 0x10 ; Бит оранжевой лампы
    red_lamp db 0x11 ; Бит красной лампы
    dac_start db 0x12 ; Бит запуска ЦАП

section .bss
    sensor_values resb 1 ; Резервирование байта для значений датчиков
    time_counter resw 1 ; Счетчик времени
    horn_index resb 1 ; Индекс для массива значений гудка

section .text
    global main_loop

main_loop:
    ; Чтение значений датчиков с порта ввода 301h
    in al, 301h
    mov [sensor_values], al

    ; Проверка уровня воды на 1 метр
    test al, 07h ; Проверяем первые три датчика
    jnz water_at_1m

    ; Выключить оранжевый сигнал, если вода не обнаружена
    mov dx, 300h
    mov ax, [sensor_values]
    and ax, 0FBh
    out dx, ax
    jmp check_water_3m

water_at_1m:
    ; Включить оранжевый сигнал
    mov al, [sensor_values]
    or al, [orange_lamp]
    mov [sensor_values], al
    mov dx, 300h
    out dx, al

check_water_3m:
    ; Проверка уровня воды на 3 метра
    mov al, [sensor_values]
    test al, 38h ; Проверяем следующие три датчика
    jnz water_at_3m

    ; Выключить красный сигнал и гудок, если вода не обнаружена
    and al, 0F3h
    mov [sensor_values], al
    mov dx, 300h
    out dx, al
    jmp update_time

water_at_3m:
    ; Включить красный сигнал и гудок
    mov al, [sensor_values]
    or al, [red_lamp]
    mov si, [horn_index]
    shl si, 1 ; Удвоение индекса для доступа к значениям типа word
    mov bx, [horn_values + si]
    or bx, [dac_start] ; Установить бит запуска ЦАП
    out dx, bx
    mov [sensor_values], al
    mov dx, 300h
    out dx, al

update_time:
    ; Увеличиваем time_counter на 1 (приращение 0.5 секунды)
    inc word [time_counter]
    cmp word [time_counter], 20 ; 20 приращений = 10 секунд
    jle main_loop

    ; Сбрасываем счетчик после 10 секунд
    mov word [time_counter], 0
    jmp main_loop
