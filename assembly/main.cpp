//
//  main.cpp
//  assembly
//
//  Created by Alexandr Kozin on 12.09.2023.
//

#include <iostream>

extern "C" void my_asm_function();

int main() {
    std::cout << "Hello from C++!" << std::endl;
    
    my_asm_function();
    
    return 0;
}
