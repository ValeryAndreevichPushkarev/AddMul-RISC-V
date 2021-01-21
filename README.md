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
