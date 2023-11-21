%include "io.inc"

section .data
    A dd 10
    B dd 10
    C dd 10

section .text
    global CMAIN

CMAIN:
    mov ebp, esp; for correct debugging
    mov eax, [B]
    mov ebx, 59
    imul ebx        ; B*59 in eax
    
    mov ebx, [C]
    add eax, ebx    
    
    mov ebx, eax    ; (B*59+C) in ebx
    
    mov eax, [A]
    mov ecx, 891
    add eax, ecx    ; A+891 in eax
    
    idiv ebx        ; (A+891/(B*59+C)) in eax
    
    mov ebx, 76
    imul ebx        ; result in eax
    
    PRINT_DEC 4, eax ; macro for print decimal value answer
    mov eax, 1
    ret
