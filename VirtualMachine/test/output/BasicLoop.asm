
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

// pop local 0
@0
D=A
@LCL
A=M
D=D+A
@temp
M=D
@SP
A=M-1
D=M
@temp
A=M
M=D
@SP
M=M-1

// label LOOP
(LOOP)

// push argument 0
@0
D=A
@ARG
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// push local 0
@0
D=A
@LCL
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// add
@SP
AM=M-1
D=M
@SP
AM=M-1
M=D+M
@SP
M=M+1

// pop local 0
@0
D=A
@LCL
A=M
D=D+A
@temp
M=D
@SP
A=M-1
D=M
@temp
A=M
M=D
@SP
M=M-1

// push argument 0
@0
D=A
@ARG
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

// sub
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M-D
@SP
M=M+1

// pop argument 0
@0
D=A
@ARG
A=M
D=D+A
@temp
M=D
@SP
A=M-1
D=M
@temp
A=M
M=D
@SP
M=M-1

// push argument 0
@0
D=A
@ARG
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

// if-goto LOOP
@SP
AM=M-1
D=M
@LOOP
D;JGT

// push local 0
@0
D=A
@LCL
D=D+M
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
(END)
@END
0;JMP