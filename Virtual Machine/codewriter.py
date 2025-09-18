

class CodeWriter():
    def __init__(self):
        pass

    def get_label(self, segment_id):
        if segment_id == 'local':
            return 'LCL'
        elif segment_id == 'argument':
            return 'ARG'
        
    def operation_commands(self, op):
        res = []

        if op == 'add':
            res.extend(['@SP', 'A=M', 'D=M', '@SP', 'M=M-1', 'A=M', 'M=M+D'])
        elif op == 'sub':
            res.extend(['@SP', 'A=M', 'D=M', '@SP', 'M=M-1', 'A=M', 'M=M-D'])
        elif op == 'neg':
            res.extend(['@SP', 'A=M', 'M=-M'])
        elif op == 'and':
            res.extend(['@SP', 'A=M', 'D=M', '@SP', 'M=M-1', 'A=M', 'M=M-D'])

        if op == 'neg':
            res.extend(['@SP', 'A=M', 'M=-M'])
        elif op == 'not':
            res.extend(['@SP', 'A=M', 'M=!M'])
        else:
            res.extend(['@SP', 'A=M', 'D=M', '@SP', 'M=M-1', 'A=M'])
            if op == 'add':
                res.append(['M=M+D'])
            elif op == 'sub':
                res.append(['M=M-D'])
            elif op == 'and':
                res.append(['M=M&D'])
            elif op == 'or':
                res.append(['M=M|D'])
            else:
                res.extend(['M=M-D', 'D=M'])

                # Setup TRUE and FALSE labels
                res.extend(['(TRUE)', '@SP', 'A=M', 'M='])

                if op == 'eq':





        return res

    def translate(self, codelist):
        asm = []
        for code in codelist:
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




