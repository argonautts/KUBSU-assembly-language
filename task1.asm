%include "io.inc"

section .data
  i1db db 70
  i1dw dw 70
  i1dd dd 70
  i2dw dw -2504
  i2dd dd -2504

section .text
    global CMAIN

CMAIN:
    mov rbp, rsp ;debug

    mov ecx, [i2dd]
    mov ebx, i2dd
    mov edi, [i1dd]
    mov [ebp+edi], ecx

    mov eax, 1
    int 0x80

