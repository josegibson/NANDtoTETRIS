@R1 // save 32769 here
D=M
@VERT
M=D

@0
A=A-1
D=A
@HORIZ
M=D

@SCREEN
M=D // first row to -1 top edge

D=A // storing screen address
@i
M=D // keeping that into i

@0
D=A
@C
M=D // keeping the index variable for the condition


(LOOP)
@i
D=M // D has the current row

@32
D=D+A // screen address + 32 for next row
@i
M=D // saving that value to i

@HORIZ // replace with VERT for hollow rectangle
D=M // holding vertical in D

@i
A=M // using the value as address
M=D // filling that address with VERT

@C
M=M+1 // incrementing
D=M

// condition to jump
@R0
D=M-D // if 0 or negative, loop ends
@LOOP
D;JGT

@i
D=M 

@32
D=D+A 
@i
M=D

@HORIZ
D=M

@i
A=M 
M=D 

(END)
@END
0;JEQ

