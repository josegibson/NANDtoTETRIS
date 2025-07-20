@R0
D=M

@prod
M=D

//init and set i = 1
@1
D=A
@i
M=D // i has 1

(LOOP)
	@R0
	D=M

	@prod
	M=D+M

	@i
	M=M+1
	D=M

	@R1
	D=D-M
	@LOOP
	D;JLT

@prod
D=M

@R2
M=D

(END)
@END
0;JEQ
	

