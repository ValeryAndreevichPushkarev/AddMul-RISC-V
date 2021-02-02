# Base AddMul Modules
Contain generator for base Add Mul commands with specified bitness.

Number of swithing transistors in add(16): 36

Number of swithing transistors in mul(16): 196


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
