
// push constant 7
@7
D=A
@SP
M=M+1
A=M
M=D

// push constant 8
@8
D=A
@SP
M=M+1
A=M
M=D

// add
@SP
A=M
D=M
@SP
M=M-1
A=M
M=D+M
(END)
@END
0;JMP