//
//  my_asm.s
//  assembly
//
//  Created by Alexandr Kozin on 12.09.2023.
//
.globl _my_asm_function

_my_asm_function:
    // Ваш ассемблерный код здесь
    // Например, можно добавить инструкцию вывода сообщения на консоль
    mov x0, x1
    ldr x1, =message
    mov x2, 13
    mov x16, 0x2
    svc 0x80
    ret

.data
message:
    .asciz "Hello from Assembly!\n"
