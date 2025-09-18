

class CodeWriter():
    def __init__(self):
        self.label_id = 0

    def get_label(self, segment_id):
        if segment_id == 'local':
            return 'LCL'
        elif segment_id == 'argument':
            return 'ARG'
        elif segment_id == 'this':
            return 'THIS'
        elif segment_id == 'that':
            return 'THAT'
        
    def get_operation_commands(self, op):
        res = []

        if op == 'neg':
            res.extend(['@SP', 'A=M-1', 'M=-M'])
        elif op == 'not':
            res.extend(['@SP', 'A=M-1', 'M=!M'])
        else:
            # op2 in D, op1 in M
            res.extend(['@SP', 'AM=M-1', 'D=M', '@SP', 'AM=M-1'])
            if op == 'add':
                res.append('M=D+M')
            elif op == 'sub':
                res.append('M=M-D')
            elif op == 'and':
                res.append('M=D&M')
            elif op == 'or':
                res.append('M=D|M')
            else:
                res.extend(['M=M-D', 'D=M'])

                if op == 'eq':
                    res.extend([f'@TRUE_{self.label_id}', 'D;JEQ'])
                elif op == 'gt':
                    res.extend([f'@TRUE_{self.label_id}', 'D;JGT'])
                elif op == 'lt':
                    res.extend([f'@TRUE_{self.label_id}', 'D;JLT'])
                
                # Setup TRUE, FALSE and CONTINUE labels
                res.extend(['@SP', 'A=M', 'M=0', f'@END_{self.label_id}', '0;JMP'])
                res.extend([f'(TRUE_{self.label_id})', '@SP', 'A=M', 'M=-1'])
                res.extend([f'(END_{self.label_id})'])
                self.label_id += 1
            res.extend(['@SP', 'M=M+1'])        
        return res

    def translate(self, codelist):
        asm = []
        for code in codelist:
            asm.append(f'\n// {code}')
            code = code.split()
            if len(code) == 1:
                asm.extend(self.get_operation_commands(code[0]))
            else:
                stk_op = code[0]
                segment = code[1]
                i = code[2]

                if stk_op == 'push':

                    # Setting the target value to D
                    asm.extend([f'@{i}', 'D=A'])
                    if segment != 'constant':
                        asm.extend([f'@{self.get_label(segment)}', 'D=D+M', 'A=D', 'D=M'])

                    # Incrementing SP and adding to stack
                    asm.extend(['@SP', 'M=M+1', 'A=M', 'M=D'])
                
                elif stk_op == 'pop':

                    # Set R6 to the destination address
                    asm.extend([f'@{i}', 'D=A', f'@{self.get_label(segment)}', 'A=M', 'D=D+A', '@R6', 'M=D'])

                    # pop the stack to D
                    asm.extend(['@SP', 'A=M', 'D=M'])

                    # Opening the address saved in R6 and setting D to it
                    asm.extend(['@R6', 'A=M', 'M=D'])  

                    # Decrement SP
                    asm.extend(['@SP', 'M=M-1'])

        asm.extend(['(END)', '@END', '0;JMP'])
        return asm
    


# cw = CodeWriter()
# cd = cw.translate([
#     'push constant 7',
#     'push constant 8',
#     'add'
# ])
# print('\n'.join(map(str, cd)))