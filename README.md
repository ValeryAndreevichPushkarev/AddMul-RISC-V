# Base AddMul Modules
Contain generator for base Add Mul commands with specified bitness.

This allows to build up to 1K cores per one chip (2k switches for most sophisticated command for 32 bit)

Total delay in transistors switches in add 32b (approx): 8
Total active logical elements in add : **216**
7 nm core freq: 41 Ghz
7 nm core power (on freq 3 Ghz): **0.0648 mW**
Total transistors in add : **55296**            

Total delay in transistors switches in mul 32b (approx): 64
Total active logical elements in mul : **2744**
7 nm core freq: 5 Ghz
7 nm core power (on freq 3 Ghz): **0.8232 mW**
Total cores, or modules (add and mul) per ~20b Transistors :24598
Total power dissipation (mW, 3 Ghz) : 22838.0376
Total transistors in mul : **702464**


Total power consumption:


3k transistor switches on 1 Ghz or so
About 1mW

# TODO:
Add RISC-V 32(64)i commands (AND\OR\XOR and so)
