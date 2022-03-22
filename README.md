# Base AddMul Modules
Contain generator for base Add Mul commands with specified bitness based on postion encoding.

This allows to build up to 1K cores per one chip (2k switches for most sophisticated command for 32 bit)

## 4 bit base (width=16):

Total delay in transistors switches in add 32b (approx): 16.0

Total active logical elements in add : 16.0

Total core power add (mW): 0.0064

Total transistors in add : 55296

Freq on 7 nm in add (Ghz) : 6.468305304010349

Total delay in transistors switches in mul 32b (approx): 19.0

Total active logical elements in mul : 88.0

Total core power mul (mW): 0.0352

Total transistors in mul : 71744.0

Freq on 7 nm in mul (Ghz) : 5.390254420008625



Total power consumption:

3k transistor switches on 1 Ghz or so
About 1mW

# TODO:
Validate new ADD/MUL modules.
Validate AND/OR/XOR modules.
Validate comparasion module.

