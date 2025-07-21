

class CodeWriter():
    def __init__(self, filename):
        self.label_id = 0
        self.filename = filename

    def get_label(self, segment_id, i):
        print (segment_id, i)
        if segment_id == 'local':
            return 'LCL'
        elif segment_id == 'argument':
            return 'ARG'
        elif segment_id == 'this':
            return 'THIS'
        elif segment_id == 'that':
            return 'THAT'
        elif segment_id == 'static':
            return f"{self.filename}.{i}"
        elif segment_id == 'pointer' and i == '0':
            return 'THIS'
        elif segment_id == 'pointer' and i == '1':
            return 'THAT'
        elif segment_id == 'temp':
            return '5'

        
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
                        if segment == 'temp':
                            asm.extend([f'@5', 'D=D+A', 'A=D', 'D=M'])
                        elif segment == 'pointer':
                            asm.extend([f'@{self.get_label(segment, i)}', 'D=M'])
                        else:
                            asm.extend([f'@{self.get_label(segment, i)}', 'D=D+M', 'A=D', 'D=M'])

                    # Incrementing SP and adding to stack
                    asm.extend(['@SP', 'A=M', 'M=D', '@SP', 'M=M+1'])
                
                elif stk_op == 'pop':

                    # temp = destination address
                    if segment == 'temp':
                        asm.extend([f'@{i}', 'D=A', '@5', 'D=D+A', '@temp', 'M=D'])
                    elif segment == 'pointer':
                        asm.extend([f'@{self.get_label(segment, i)}', 'D=A', '@temp', 'M=D'])
                    else:
                        asm.extend([f'@{i}', 'D=A', f'@{self.get_label(segment, i)}', 'A=M', 'D=D+A', '@temp', 'M=D'])

                    # pop the stack to D
                    asm.extend(['@SP', 'A=M-1', 'D=M'])

                    # Opening the address saved in temp and setting D to it
                    asm.extend(['@temp', 'A=M', 'M=D'])  

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