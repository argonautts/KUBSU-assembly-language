%include "io.inc"

section .data
    A dd 10
    B dd 10
    C dd 10
    RESULT dd 0

section .text
    global CMAIN

CMAIN:
    mov eax, [B]	;12+5
    mov ebx, 59	;4
    imul ebx        	;154

    mov ebx, [C]	;12+5
    add eax, ebx	;3

    mov ebx, eax    ; 4

    mov eax, [A]	;12+5
    mov ecx, 891	;4
    add eax, ecx	;3

    idiv ebx        ; 184

    mov ebx, 76 ;4
    imul ebx        ; 154

    PRINT_DEC 4, eax 	;
    mov ebx, 1	;4
    and ebx, edx	;3

    jz is_zero		;15

    mov eax, 0	;4
    mov [RESULT], eax	;13+5

    mov eax, 1	;4
    ret

is_zero:
    mov eax, 1			;4
    mov [RESULT], eax	;13+5
