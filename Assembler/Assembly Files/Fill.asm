@8192 // defining end
D=A
@SCREEN
D=D+A
@end
M=D


@0 // defining black
D=A-1
@black
M=D

@0 // defining white
D=A
@white
M=D
@with
M=D


(SCAN)
@KBD
D=M

@FILL
D;JGT

@EMPTY
D;JEQ

@SCAN
0;JEQ // continue loop

(FILL) // filler
@black
D=M
@with
M=D
@ROLL
0;JMP

(EMPTY) // unfiller
@white
D=M
@with
M=D
@ROLL
0;JMP

(ROLL)
@SCREEN
D=A
@CURR
M=D

(LOOP)
@with
D=M
@CURR
A=M //dereferencing
M=D

@CURR
M=M+1
D=M

@end
D=D-M
@LOOP
D;JLT


@SCAN // go back to scan
0;JEQ

