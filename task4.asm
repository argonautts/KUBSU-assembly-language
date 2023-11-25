%include "io.inc" 

section .data 
    USRRS dw 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0	
    AINS db 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0		
    RC db 10 						
    AIN dw 0000001000101001b  			
    USRR dw 0001110000000100b 		
    Udelta db 11h 					
    SR_MASK db 11000000b
    SR_INV_MASK db 00111111b 		
    RS_MASK db 00000001b
    RS_INV_MASK db 11111110b    		

section .text 
global CMAIN 

; Подпрограмма для проверки необходимости обработки итерации
check_rc_success:
    mov dx, [AIN]
    test bx, 1    			; Проверка бита четности итерации
    jne is_odd    			; Переход к обработке нечетного случая
    jmp is_even  			; Переход к обработке четного случая

; Подпрограмма для обработки нечетного случая
is_odd:  	
    or al, [SR_MASK]		; Устанавливаем биты SR
    and al, [RS_INV_MASK] 	;Сбрасываем биты RS
    call save_usrrt
    ret

; Подпрограмма для обработки четного случая
is_even:
    or al, [RS_MASK]		; Устанавливаем биты RS
    and al, [SR_INV_MASK]	; Сбрасываем биты SR
    call save_usrrt
    ret

; Сохранение модифицированного значения УСРР и вызов задержки
save_usrrt:
    mov [esi], ax  		; Сохранение УСРР в массив
    ;out 080h, ax  		; Вывод УСРР на устройство вывода 
    call delay  			; Вызов задержки
    ret

; Функция задержки
delay:
    mov ECX, 44800  	; Установка счетчика цикла задержки 44,8 мс
start_loop:
    loop start_loop  		; Выполнение цикла задержки

; Сохранение информации о кнопках A_in
save_ain:
    mov [edi], dl

; Увеличение старшего байта УСРР
incUSRR:
    add ah, [Udelta]  		; Добавление к старшему байту УСРР значения Udelta
    ret

; Основная функция программы
CMAIN:
    mov ebp, esp 		; Установка базового указателя для отладки
    mov ax, [USRR]  	; Загрузка начального значения УСРР
    mov dx, [AIN]  		; Загрузка начального значения A_in
    mov bx, 11  		; Установка размера обрабатываемого массива
    mov esi, USRRS  	; Указатель на начало массива USRRS
    mov edi, AINS  		; Указатель на начало массива AINS

; Основной цикл программы
main_loop:
    ;in dx, 07Fh  		; Чтение данных с порта
    mov dx, [AIN]
    inc dx  			; Инкремент A_in
    mov [AIN], dx
    mov cl, [RC]
    shr dx, cl  			; Сдвиг A_in на количество битов, указанное в RC

    call check_rc_success  	; Вызов подпрограммы проверки

    add esi, 2  			; Переход к следующему элементу в массиве USRRS
    add edi, 1  			; Переход к следующему элементу в массиве AINS

    dec bx  			; Уменьшение счетчика цикла
    cmp bx, 0
    je main_loop_end  	; Завершение цикла, если счетчик равен нулю
    jmp main_loop  		; Повтор цикла

; Завершение программы
main_loop_end:
    xor eax, eax
    xor ebx, ebx
    int 0x80  			; Системный вызов для завершения программы

