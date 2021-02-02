#version with positional digits encoding
#width - numeric range for operation
import math
#command names
op_names = ["add","mul","sub","div","pow","act_func","act_func_2_1"]
#input registers
width = 16;
#maximum used commands in module (set to one for implement one function)
op_count = 2;

#Specified if Intel quartus used, in that case module works from module_generator
Quartus_used = False

#Number of modules in one computation Unit (heght)
NumOfModules = 20

#Generate add\mul modules up to 32 bit
GenerateMulAdd=1
#Target bitness for superior IP core
target_MulAdd_bitness = 16

#variables for IP core generation
RecursionLevel = int(math.log(target_MulAdd_bitness/math.log(width,2),2))
baseBitness = int(math.log(width,2))


print("Total delay in transistors switches in add "+str(target_MulAdd_bitness)+"b (approx): " + str(2**(RecursionLevel)))
print("Total active logical elements in add : " + str(6**(RecursionLevel)))


print("Total delay in transistors switches in mul "+str(target_MulAdd_bitness)+"b (approx): " + str(4**(RecursionLevel)))
print("Total active logical elements in mul : " + str(14**(RecursionLevel)))


#TODO:
##Number of Units in one computation Core (width)
#NumOfUnits = 10

maxnum=width;
output_width = 2*width;
maxoutputnum = width*width;

def positionEncToBinary(width, lineName,delta):
	base_bitness = int(math.log(width,2))
	formatStr = '{:0'+str(base_bitness)+'b}'
	resultEq = ""

	for j in range(base_bitness):
		for i in range(2**base_bitness):
			result = list(formatStr.format(i))
			somethingToAdd = 0
			if result[j] == '1':
				somethingToAdd = 1
				resultEq = resultEq + lineName+"["+str(i+delta)+"]"
			if (i==2**base_bitness-1)&(somethingToAdd==1)&(j!=base_bitness-1):
				resultEq = resultEq + ",\r\n"
			else:
				if (somethingToAdd == 1)&(i!=2**base_bitness-1):
					resultEq = resultEq + "|"
	return "{"+resultEq+"}"

def op1(x, y):
	return int(math.fmod(x+y,maxoutputnum))

def op2(x, y):
	return int(math.fmod(x*y,maxoutputnum))
def op3(x, y):
	return x*width+y

def op4(x, y):
	return int(math.fmod(x/(y+1),maxoutputnum))

def op5(x, y):
	return int(math.fmod(x**y,maxoutputnum))
def op6(x, y):
	return int(math.fmod(1/(math.exp(x)+1),maxoutputnum))
def op7(x, y):
	return int(math.fmod(1/(math.exp(x)+1),maxoutputnum))

def formatNum(x):
	result = '1'
	for i in range(x):
		result = result +"0"
	for i in range(width-x-1):
		result = "0" + result
	return 	result 

def formatOutputNum(x):
	result = '1'
	c1 = x%width
	c2 = int(math.floor(x/width))
	for i in range(c1):
		result = result +"0"
	for i in range(width-c1-1):
		result = "0" + result

	result2 = '1'
	for i in range(c2):
		result2 = result2 +"0"
	for i in range(width-c2-1):
		result2 = "0" + result2

	return 	result2+ result 
header = """module """+op_names[0]+"""
(
"""
for i in range(op_count):
	header = header + "	input wire " + op_names[i] +",\r\n"

header = header + """
	input wire[""" +str(width-1)+ """:0] r1,
	input wire[""" +str(width-1)+ """:0] r2,
	output wire[""" +str(output_width-1)+ """:0] output_reg
);
"""

# Write the file out again
with open('output.txt', 'w') as file:
	file.write(header)
	for i in range(maxnum):
				for j in range(maxnum):
					file.write("wire input_"+str(i)+"_"+str(j)+" = r1["+str(i)+"]&r2["+str(j)+"];\r\n")


	for command in range(op_count):
		for bitnum in range(output_width):
				has_any_one = 0
				predicate = "wire command_" + op_names[command] +"_"+str(bitnum)+" = "
				val = op_names[command]+"&("
				for i in range(maxnum):
					for j in range(maxnum):
						op1_result = 0
						op1_result = op1(i,j)
						op2_result = 0
						op2_result= op2(i,j)
						op3_result = 0
						op3_result= op3(i,j)
						op4_result = 0
						op4_result= op4(i,j)
						op5_result = 0
						op5_result= op5(i,j)
						op6_result = 0
						op6_result= op6(i,j)
						op7_result = 0
						op7_result= op7(i,j)

						b_op1_result =  list(formatOutputNum(op1_result))
						b_op2_result =  list(formatOutputNum(op2_result))
						b_op3_result =  list(formatOutputNum(op3_result))
						b_op4_result =  list(formatOutputNum(op4_result))
						b_op5_result =  list(formatOutputNum(op5_result))
						b_op6_result =  list(formatOutputNum(op6_result))
						b_op7_result =  list(formatOutputNum(op7_result))


						op_results = [
						b_op1_result[bitnum],
						b_op2_result[bitnum],
						b_op3_result[bitnum],
						b_op4_result[bitnum],
						b_op5_result[bitnum],
						b_op6_result[bitnum],
						b_op7_result[bitnum]]
						
						
						if (op_results[command]=='1'):

							if (has_any_one==1):
								val = val +"|"
							has_any_one = 1
							#write a part of equation

							val = val + "input_"+str(i)+"_"+str(j)
				if (has_any_one):
					file.write(predicate+val + ");"+ "\r\n")
				else:
					file.write(predicate+" 0;\r\n")
											

	file.write("assign output_reg = {")
	for bitnum in range(output_width):
		for command in range(op_count):
			file.write("command_" + op_names[command] +"_"+str(bitnum))
			if (command!=op_count-1):
				file.write("|")
		file.write(",\r\n")
			
	file.write("}\r\nendmodule\r\n")
with open('output.txt', 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace(',,', ',')
filedata = filedata.replace(',\r\n}', '};')
# Write the file out again
with open('output.txt', 'w') as file:
  file.write(filedata)
with open('output.txt', 'w') as file:
  file.write(filedata)


#
#Write computation unit with specified number of computation modules
#TODO: add 4-8 int 16-32 float operations instead of command_name lines
#
with open('output.txt', 'r') as file :
  filedata = file.read()
with open('output.txt', 'w') as file:
	header = """module computationUnit_"""+op_names[0] +"""
(
"""
	for i in range(op_count):
		header = header + "	input wire ["+str(NumOfModules)+":0]" + op_names[i] +",\r\n"

	header = header + """
	input wire["""+str(width*NumOfModules)+""":0] r1_bus,
	input wire["""+str(width*NumOfModules)+""":0] r2_bus,
	
	output wire["""+str(2*width*NumOfModules)+""":0] r_result_bus
);\r\n"""
	for i in range(NumOfModules):
		header = header + op_names[0]+ " " + op_names[0]+str(i)+"("
		for j in range(op_count):
			header = header + op_names[j] + "["+str(i)+"], "
		header = header + "r1_bus["+str((i+1)*width-1)+":"+str(i*width)+"],"
		header = header + "r2_bus["+str((i+1)*width-1)+":"+str(i*width)+"],"
		header = header + "r_result_bus["+str((i+1)*2*width-1)+":"+str(i*2*width)+"]);\r\n"
	header = header + "endmodule\r\n"
	file.write(filedata + header)
	

#
#
#Writes code to generate one computation module
#
#

with open('output.txt', 'r') as file :
  filedata = file.read()
with open('output.txt', 'w') as file:
	busLen = width
	header = """module module_generator_"""+op_names[0] +"""
(
	input wire clk,"""
	if (Quartus_used):
		header = header + """
	input wire generator_use,
	input wire ["""+str(op_count-1)+""":0] op_selector_data,
	input wire ["""+str(width-1)+""":0] r1_data,
	input wire ["""+str(width-1)+""":0] r2_data,
	output wire ["""+str(2*width-1)+""":0] r_out,"""
	header = header +"""
	output wire["""+str(2*width-1)+""":0] r_result
);
reg["""+str(width-1)+""":0] r1=1'b1;
reg["""+str(width-1)+""":0] r2=1'b1;
reg["""+str(op_count-1)+""":0] op_selector=1'b0001;"""
	if (Quartus_used):
		header = header + """
wire["""+str(width-1)+""":0] r1_input = {"""
		for i in range(width):
			header = header + """(r1["""+str(i)+"]&generator_use)|(r1_data["+str(i)+"]&(~generator_use))"""
			if (i!= width-1):
				header = header + ","
			else:
				header = header + "};\r\n"
		header = header + """wire["""+str(width-1)+""":0] r2_input = {"""
		for i in range(width):
			header = header + """(r2["""+str(i)+"]&generator_use)|(r2_data["+str(i)+"]&!(~generator_use))"""
			if (i!= width-1):
				header = header + ","
			else:
				header = header + "};\r\n"

		header = header + """wire["""+str(op_count-1)+""":0] op_selector_input = {"""
		for i in range(op_count):
				header = header + """(op_selector["""+str(i)+"]&generator_use)|(op_selector_data["+str(i)+"]&(~generator_use))"""
				if (i!= op_count-1):
					header = header + ","
				else:
					header = header + "};\r\n"
	if (Quartus_used):
		header = header + """
	""" + op_names[0] +""" CM ("""
		for i in range(op_count):
			header = header + "op_selector_input["+str(i)+"],"
		header = header + """r1_input,r2_input,r_result);"""
	else:
		header = header + """
	""" + op_names[0] +""" CM ("""
		for i in range(op_count):
			header = header + "op_selector["+str(i)+"],"
		header = header + """r1,r2,r_result);"""
	#generate states for first op_selector


	header = header + """
assign r_out = r_result;

always@(posedge clk"""
	if (Quartus_used):
		header = header + """&generator_use)"""
	else:
		header = header + """)"""
	header = header + """
begin
"""
	header = header + "	r1<={r1[0],"""
	for j in range(width-1):
		header = header + """r1["""+str(width-j-1)+"""]"""
		if j!= width-2:
			header = header +","

	header = header + "};"
	header = header + """
	if (r1["""+str(width-1)+"""]==1'b1)
"""
	header = header + "		r2<={r2[0],"""
	for j in range(width-1):
		header = header + """r2["""+str(width-j-1)+"""]"""
		if j!= width-2:
			header = header +","

	header = header + "};"
	header = header + """
	if (r2["""+str(width-1)+"""]==1'b1)
"""
	header = header + "		op_selector<={op_selector[0],"""
	for j in range(op_count-1):
		header = header + """op_selector["""+str(op_count-j-1)+"""]"""
		if j!= op_count-2:
			header = header +","

	header = header + "};"
	header = header + """
end
"""
	
	header = header + "endmodule\r\n"
	file.write(filedata + header)

#	
#
#Writes code to generate one computation unit
#
#


with open('output.txt', 'r') as file :
  filedata = file.read()
with open('output.txt', 'w') as file:
	busLen = width*NumOfModules
	header = """module core_generator_"""+op_names[0] +"""
(
	input wire clk,
	output wire["""+str(2*busLen)+""":0] r_result_bus
);
"""
	for i in range (NumOfModules):
		header = header + "reg["+str(width)+":0] r1"+str(i)+"=1'b1;\r\n"
		header = header + "reg["+str(width)+":0] r2"+str(i)+"=1'b1;\r\n"

	
	for i in range(NumOfModules):
		header = header + "reg["+str(op_count)+":0] op_selector"+str(i)+"=1'b0001;\r\n"

	header = header + """computationUnit_"""+op_names[0] +""" CU ("""
	for j in range(op_count):
		header = header + "{"
		for i in range(NumOfModules):
			header = header + "op_selector"+str(i)+"["+str(j)+"]"
			if (i!=NumOfModules-1):
				header = header + ","
		header = header + "},"
	header = header +"{"
	for i in range (NumOfModules):
		header = header + "r1"+str(i)
		if (i!=NumOfModules-1):
			header = header + ","
	header = header + "},{"
	for i in range (NumOfModules):
		header = header + "r2"+str(i)
		if (i!=NumOfModules-1):
			header = header + ","

	header = header +"},r_result_bus);"
	#generate states for first op_selector

	for i in range (NumOfModules):
		if (i==0):
			header = header + """
always@(posedge clk)
begin
"""
		else:
			header = header + """
always@(posedge r2"""+str(i-1)+"""["""+str(width-1)+"""])
begin
"""
		header = header + "	r1"+str(i)+"<={r1"""+str(i)+"""[0],"""
		for j in range(width-1):
			header = header + """r1"""+str(i)+"""["""+str(width-j-1)+"""]"""
			if j!= width-2:
				header = header +","

		header = header + "};\r\n"
		header = header + """	if (r1"""+str(i)+"""["""+str(width-1)+"""]==1'b1)\r\n"""

		header = header + "		r2"+str(i)+"<={r2"""+str(i)+"""[0],"""
		for j in range(width-1):
			header = header + """r2"""+str(i)+"""["""+str(width-j-1)+"""]"""
			if j!= width-2:
				header = header +","

		header = header + "};\r\n"
		header = header + """	if (r2"""+str(i)+"""["""+str(width-1)+"""]==1'b1)\r\n"""
		header = header + "		op_selector"+str(i)+"<={op_selector"""+str(i)+"""[0],"""
		for j in range(op_count-1):
			header = header + """op_selector"""+str(i)+"""["""+str(op_count-j-1)+"""]"""
			if j!= op_count-2:
				header = header +","

		header = header + "};"
		header = header + """
end
"""
	
	header = header + "endmodule\r\n"
	file.write(filedata + header)


#Write converter from binary to positional for base bitness

with open('output.txt', 'r') as file :
  filedata = file.read()
with open('output.txt', 'w') as file:
	busLen = width

	input_reg = width*(2**RecursionLevel)
	output_reg = 2*input_reg
	base_bitness = int(math.log(width,2))

	formatStr = '{:0'+str(base_bitness)+'b}'

	header = """module converter_"""+str(base_bitness) +"""
(
	
	input wire["""+ str(int(2*width)-1)+""":0] r_res,
	input wire["""+str(base_bitness-1)+""":0] r1_binary,
	input wire["""+str(base_bitness-1)+""":0] r2_binary,
	output wire["""+ str(int(width)-1)+""":0] r1,
	output wire["""+ str(int(width)-1)+""":0] r2,
	output wire["""+ str(2*base_bitness-1)+""":0] r_res_binary
);
"""
	#convert binary to positional encoding
	for j in range(width):
			header = header + """
	assign r1["""+str(j)+"""] = (r1_binary["""+str(base_bitness-1)+""":0]=="""+str(base_bitness)+"""'b"""+formatStr.format(j)+""") ?1'b1:1'b0;"""
			

	for j in range(width):
			header = header + """
	assign r2["""+str(j)+"""] = (r2_binary["""+str(base_bitness-1)+""":0]=="""+str(base_bitness)+"""'b"""+formatStr.format(j)+""") ?1'b1:1'b0;"""

	#convert positional encoding to binary
	header = header + """

	assign r_res_binary = {"""

	for i in reversed(range(2)):
		header = header + positionEncToBinary(width, "r_res", i*width) 
		if (i!=0):
			header = header + ",\r\n\r\n"
		else:
			header = header + "};\r\n"
	

	header = header + "endmodule\r\n"
	file.write(filedata + header)



#Generate add/mul modules up to specified bitness
if (GenerateMulAdd==1):
	for i in range(RecursionLevel):
		with open('output.txt', 'r') as file :
		  filedata = file.read()
		with open('output.txt', 'w') as file:
			#generate ADD module
			add_mul_base_module_name = "add_"+str(baseBitness*2**(i))
			add_prefix = "(1,0,"
			mul_prefix = "(0,1,"
			#use base module
			if (i==0):
				add_mul_base_module_name = op_names[0]
				add_prefix = "(1,0,"
				mul_prefix = "(0,1,"
			else:
				add_prefix = "("
				mul_prefix = "("
			input_width = width*2**(i+1)
			output_width = 2*input_width
			header = """\r\nmodule add_"""+str(baseBitness*2**(i+1)) +"""
		(
			input wire["""+str(input_width-1)+""":0] r1,
			input wire["""+str(input_width-1)+""":0] r2,
			output wire["""+str(output_width-1)+""":0] r_result
		);
		"""
			#get wirings 
			for j in range(4):
				header = header + """
			wire ["""+str(input_width/2-1)+""":0] d"""+str(j)+"""= """
				if (j<2):
					header = header + "r1"
				else:
					header = header + "r2"
				header = header + "["+str((j%2+1)*input_width/2 -1)+":"+str((j%2)*input_width/2)+"];"
			#wiring for temporal results
			for j in range(8):
				header = header + """
			wire ["""+str(input_width/2-1)+""":0] dt"""+str(j)+""";"""
			header = header + """
			
			
			 """+add_mul_base_module_name+""" mod1_"""+str(j)+add_prefix
					#supress other comman lines
			for k in range(op_count-2):
				header = header + "0,"

			header = header + """d0,d2,{dt2,dt0});""" +"""
			
			 """+add_mul_base_module_name+""" mod2_"""+str(j)+add_prefix
					#supress other comman lines
			for k in range(op_count-2):
				header = header + "0,"

			header = header + """d1,d3,{dt3,dt1});
		

			 """+add_mul_base_module_name+""" mod3_"""+str(j)+add_prefix
					#supress other comman lines
			for k in range(op_count-2):
				header = header + "0,"

			header = header + """dt1,dt2,{dt5,dt4});

			 """+add_mul_base_module_name+""" mod4_"""+str(j)+add_prefix 
					#supress other comman lines
			for k in range(op_count-2):
				header = header + "0,"

			header = header + """dt5,dt3,{dt7,dt6});"""
		

			header = header + """
			assign r_result = {dt7,dt6,dt4,dt0};
	endmodule

	"""
			#Generate MUL module
			mul_base_module_name = "mul_"+str(baseBitness*2**(i))
			add_base_module_name = "add_"+str(baseBitness*2**(i))
			#use base module
			if (i==0):
				add_base_module_name = op_names[0]
				mul_base_module_name = op_names[0]
			if (i==0):
				add_prefix = "(1,0,"
				mul_prefix = "(0,1,"
			else:
				add_prefix = "("
				mul_prefix = "("
			input_width = width*2**(i+1)
			output_width = 2*input_width
			header = header + """\r\nmodule mul_"""+str(baseBitness*2**(i+1)) +"""
		(
			input wire["""+str(input_width-1)+""":0] r1,
			input wire["""+str(input_width-1)+""":0] r2,
			output wire["""+str(output_width-1)+""":0] r_result
		);
		"""
			#get wirings 
			for j in range(4):
				header = header + """
			wire ["""+str(input_width/2-1)+""":0] d"""+str(j)+"""= """
				if (j<2):
					header = header + "r1"
				else:
					header = header + "r2"
				header = header + "["+str((j%2+1)*input_width/2 -1)+":"+str((j%2)*input_width/2)+"];"
			#wiring for temporal results
			for j in range(28):
				header = header + """wire ["""+str(input_width/2-1)+""":0] dt"""+str(j)+""";\r\n"""


			header = header + """
			//mul
			"""+mul_base_module_name+""" mod1_1 """ + mul_prefix 
					#supress other comman lines
			for k in range(op_count-2):
				header = header + "0,"

			header = header + """d0,d2,{dt1,dt0});
			
			"""+mul_base_module_name+""" mod1_2 """ + mul_prefix
					#supress other comman lines
			for k in range(op_count-2):
				header = header + "0,"

			header = header + """d1,d2,{dt3,dt2});

			"""+mul_base_module_name+""" mod1_3 """ + mul_prefix
					#supress other comman lines
			for k in range(op_count-2):
				header = header + "0,"

			header = header + """d0,d3,{dt5,dt4});

			 """+mul_base_module_name+""" mod1_4 """ + mul_prefix
					#supress other comman lines
			for k in range(op_count-2):
				header = header + "0,"

			header = header + """d1,d3,{dt7,dt6});
			
			//add
			 """+add_base_module_name+""" mod1_5 """ + add_prefix
					#supress other comman lines
			for k in range(op_count-2):
				header = header + "0,"

			header = header + """dt1,dt2,{dt9,dt8});
			 """+add_base_module_name+""" mod1_6 """ + add_prefix
					#supress other comman lines
			for k in range(op_count-2):
				header = header + "0,"

			header = header + """dt8,dt4,{dt11,dt10});
			 """+add_base_module_name+""" mod1_7 """ + add_prefix
					#supress other comman lines
			for k in range(op_count-2):
				header = header + "0,"

			header = header + """dt11,dt3,{dt13,dt12});
			 """+add_base_module_name+""" mod1_8 """ + add_prefix
					#supress other comman lines
			for k in range(op_count-2):
				header = header + "0,"

			header = header + """dt5,dt6,{dt15,dt14});
			 """+add_base_module_name+""" mod1_9 """ + add_prefix
					#supress other comman lines
			for k in range(op_count-2):
				header = header + "0,"

			header = header + """dt12,dt14,{dt17,dt16});
			 """+add_base_module_name+""" mod1_10 """ + add_prefix
					#supress other comman lines
			for k in range(op_count-2):
				header = header + "0,"

			header = header + """dt16,dt9,{dt19,dt18});
		
			 """+add_base_module_name+""" mod1_11 """ + add_prefix
					#supress other comman lines
			for k in range(op_count-2):
				header = header + "0,"

			header = header + """dt17,dt13,{dt21,dt20});

			 """+add_base_module_name+""" mod1_12 """ + add_prefix
					#supress other comman lines
			for k in range(op_count-2):
				header = header + "0,"

			header = header + """dt15,dt19,{dt23,dt22});

			 """+add_base_module_name+""" mod1_13 """ + add_prefix
					#supress other comman lines
			for k in range(op_count-2):
				header = header + "0,"

			header = header + """dt20,dt7,{dt25,dt24});

			 """+add_base_module_name+""" mod1_14 """ + add_prefix
					#supress other comman lines
			for k in range(op_count-2):
				header = header + "0,"

			header = header + """dt24,dt22,{dt27,dt26});

			assign r_result = {dt26,dt18,dt10,dt0};


	endmodule

	"""



			file.write(filedata + header)

#Write converter from binary to positional encoding 

with open('output.txt', 'r') as file :
  filedata = file.read()
with open('output.txt', 'w') as file:
	busLen = width
	input_reg = width*(2**RecursionLevel)
	output_reg = 2*input_reg
	base_bitness = int(math.log(width,2))

	formatStr = '{:0'+str(base_bitness)+'b}'

	header = """module converter_"""+str(target_MulAdd_bitness) +"""
(
	
	input wire["""+ str(int(output_reg)-1)+""":0] r_res,
	input wire["""+str(target_MulAdd_bitness-1)+""":0] r1_binary,
	input wire["""+str(target_MulAdd_bitness-1)+""":0] r2_binary,
	output wire["""+ str(int(input_reg)-1)+""":0] r1,
	output wire["""+ str(int(input_reg)-1)+""":0] r2,
	output wire["""+ str(2*target_MulAdd_bitness-1)+""":0] r_res_binary
);
"""
	#convert binary to positional encoding
	for i in range(2**RecursionLevel):
		for j in range(width):
			header = header + """
	assign r1["""+str(i*width+j)+"""] = (r1_binary["""+str((i+1)*base_bitness-1)+""":"""+str((i)*base_bitness)+"""]=="""+str(base_bitness)+"""'b"""+formatStr.format(j)+""") ?1'b1:1'b0;"""
		
	for i in range(2**RecursionLevel):
		for j in range(width):
			header = header + """
	assign r2["""+str(i*width+j)+"""] = (r2_binary["""+str((i+1)*base_bitness-1)+""":"""+str((i)*base_bitness)+"""]=="""+str(base_bitness)+"""'b"""+formatStr.format(j)+""") ?1'b1:1'b0;"""

	#convert positional encoding to binary
	header = header + """

	assign r_res_binary = {"""
	for i in reversed(range(output_reg/width)):
		header = header + positionEncToBinary(width, "r_res",i*width) 

		if (i!=0):
			header = header + ",\r\n\r\n"
		else:
			header = header + "};\r\n"
	#	for j in range(width):
	print()					

	header = header + "endmodule\r\n"
	file.write(filedata + header)

		
#
#Write module with specified number of computation units
#

#Write sram memory block's
#source sram, dest sram, module thats change two blocks after computation complete and change wirings according to bitness )
#
