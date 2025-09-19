
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// eq
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@StackTest_TRUE_0
D;JEQ
@SP
A=M
M=0
@StackTestEND_0
0;JMP
(StackTest_TRUE_0)
@SP
A=M
M=-1
(StackTestEND_0)
@SP
M=M+1

// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1

// eq
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@StackTest_TRUE_1
D;JEQ
@SP
A=M
M=0
@StackTestEND_1
0;JMP
(StackTest_TRUE_1)
@SP
A=M
M=-1
(StackTestEND_1)
@SP
M=M+1

// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// eq
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@StackTest_TRUE_2
D;JEQ
@SP
A=M
M=0
@StackTestEND_2
0;JMP
(StackTest_TRUE_2)
@SP
A=M
M=-1
(StackTestEND_2)
@SP
M=M+1

// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@StackTest_TRUE_3
D;JLT
@SP
A=M
M=0
@StackTestEND_3
0;JMP
(StackTest_TRUE_3)
@SP
A=M
M=-1
(StackTestEND_3)
@SP
M=M+1

// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@StackTest_TRUE_4
D;JLT
@SP
A=M
M=0
@StackTestEND_4
0;JMP
(StackTest_TRUE_4)
@SP
A=M
M=-1
(StackTestEND_4)
@SP
M=M+1

// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@StackTest_TRUE_5
D;JLT
@SP
A=M
M=0
@StackTestEND_5
0;JMP
(StackTest_TRUE_5)
@SP
A=M
M=-1
(StackTestEND_5)
@SP
M=M+1

// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// gt
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@StackTest_TRUE_6
D;JGT
@SP
A=M
M=0
@StackTestEND_6
0;JMP
(StackTest_TRUE_6)
@SP
A=M
M=-1
(StackTestEND_6)
@SP
M=M+1

// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

// gt
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@StackTest_TRUE_7
D;JGT
@SP
A=M
M=0
@StackTestEND_7
0;JMP
(StackTest_TRUE_7)
@SP
A=M
M=-1
(StackTestEND_7)
@SP
M=M+1

// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// gt
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@StackTest_TRUE_8
D;JGT
@SP
A=M
M=0
@StackTestEND_8
0;JMP
(StackTest_TRUE_8)
@SP
A=M
M=-1
(StackTestEND_8)
@SP
M=M+1

// push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 53
@53
D=A
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

// push constant 112
@112
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

// neg
@SP
A=M-1
M=-M

// and
@SP
AM=M-1
D=M
@SP
AM=M-1
M=D&M
@SP
M=M+1

// push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1

// or
@SP
AM=M-1
D=M
@SP
AM=M-1
M=D|M
@SP
M=M+1

// not
@SP
A=M-1
M=!M
(END)
@END
0;JMP