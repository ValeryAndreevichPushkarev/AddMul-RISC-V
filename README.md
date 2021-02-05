# Base AddMul Modules
Contain generator for base Add Mul commands with specified bitness.

This allows to build up to 1K cores per one chip (2k switches for most sophisticated command for 32 bit)

Total delay in transistors switches in add 32b (approx): 8
Total active logical elements in add : 216
Total transistors in add : 55296



Total delay in transistors switches in mul 32b (approx): 64
Total active logical elements in mul : 2744
Total transistors in mul : 702464



# TODO:

Convert those generator to tree for any function

# TreeFunc
Represent any function with a tree of subfunc with fixed len/bitness

			a				
			|				
	b	-	op1				
			|				
	c	-	op2		Rt=OP2(OP1;c)	      OR, all results from c with op3 known	op2 can be determined
			|				
	d	-	op3		R=OP3(OP2;d)	      OR, all results from d	op3 can be determined
			|				
			r				
							
f(ab,cd) = r4r3r2r1
