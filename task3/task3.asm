%include "io.inc"

section .bss
    i: resw 1
    j: resw 1
    avg: resw 1

section .data
    A dw 3,4,8,7,6,5,1,2,3,4,8,7,6,5,9,9,9,9,0,0,0,0,6,5,4,3,2,1,1,2,4,4
    B dw 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    len dw 32

section .text
    global CMAIN


CMAIN:
    mov ebp, esp			; for correct debugging
    
    xor ecx, ecx
    xor eax, eax

sum_loop:				; Цикл для вычисления суммы массива A
    xor ebx, ebx
    mov bx, [A + 2 * ecx]
    add eax, ebx
    
    ; Вычисление среднего значения
    inc ecx
    cmp ecx, [len]
    jl sum_loop
    
    xor edx, edx
    mov ebx, [len]
    idiv ebx    
    mov word[avg], ax
            
    ; Сброс значений регистров
    xor ecx, ecx
    xor ebx, ebx

new_arr_loop:			; Цикл для создания нового массива B 

        xor eax, eax
        mov ax, [A + 2 * ecx]
        
        cmp ax, word[avg]
        jle skip_add
        mov [B + 2 * ebx], ax
        inc ebx
    skip_add:
    
    inc ecx
    cmp ecx, [len]
jl new_arr_loop

; Сортировка массива B по возрастанию
    movzx ecx, word[len]		
    mov ebx, B   

i_loop:
    mov word[j], 0
    j_loop:
        mov ebx, B
        movzx eax, word[j]
        add ebx, eax
        mov eax, ebx
        add eax, 2
        mov dx, word[ebx]
        mov cx, word[eax]
        cmp cx, dx
        jl swap
        jmp skip
  
    swap:
        mov word[ebx], cx
        mov word[eax], dx

    skip:
        add word[j], 2
        mov ax, word[len]
        add ax, word[len]
        sub ax, word[i]
        sub ax, 1        
        cmp [j], ax
    jl j_loop

    inc word[i]
    mov ax, word[len]
    cmp word[i], ax

jl i_loop

    ; Изменение байтов неотрицательных элементов в массиве B
    xor ecx, ecx

swap_loop:
    xor eax, eax
    mov ax, [B + 2 * ecx]

    cmp ax, 0
    jle skip_swap
        rol ax, 8
        mov [B + 2 * ecx], ax
    skip_swap:
    inc ecx
    cmp ecx, [len]
    jl swap_loop

    xor ecx, ecx
    xor eax, eax
    mov edx, [len]

print_loop:
    xor ebx, ebx
    mov bx, [B + 2 * ecx]
    PRINT_DEC 2, bx
    PRINT_CHAR 0x20
    
    inc ecx
    cmp ecx, edx
    jl print_loop

    mov eax, 1
    int 0x80
