//
//  main.cpp
//  assembly
//
//  Created by Alexandr Kozin on 12.09.2023.
//

#include <iostream>
using namespace std;

extern "C" void start();

int main() {
    cout << "Hello from C++!" << endl;
    
    start();
    
    return 0;
}
