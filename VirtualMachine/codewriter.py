

class CodeWriter():
    def __init__(self, filename):
        self.label_id = 0
        self.filename = filename

    def get_label(self, segment_id, i):

        self.label = {
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT',
            ('pointer', '0'): 'THIS',
            ('pointer', '1'): 'THAT',
            'temp': '5' 
        }
        
        if segment_id == 'static':
            return f"{self.filename}.{i}"
        elif segment_id == 'pointer':
            return self.label[(segment_id, i)]
        else:
            return self.label[segment_id]
        
    def translate_arthmetic_commands(self, op):
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
    
    def _translate_memory_commands(self, instruction):
        res = []
        stk_op = instruction[0]
        segment = instruction[1]
        i = instruction[2]

        if stk_op == 'push':
            # Setting the target value to D
            res.extend([f'@{i}', 'D=A'])
            if segment != 'constant':
                if segment == 'temp':
                    res.extend([f'@5', 'D=D+A', 'A=D', 'D=M'])
                elif segment == 'pointer':
                    res.extend([f'@{self._get_label(segment, i)}', 'D=M'])
                else:
                    res.extend([f'@{self._get_label(segment, i)}', 'D=D+M', 'A=D', 'D=M'])
            # Incrementing SP and adding to stack
            res.extend(['@SP', 'A=M', 'M=D', '@SP', 'M=M+1'])
        
        elif stk_op == 'pop':
            # temp = destination address
            if segment == 'temp':
                res.extend([f'@{i}', 'D=A', '@5', 'D=D+A', '@temp', 'M=D'])
            elif segment == 'pointer':
                res.extend([f'@{self._get_label(segment, i)}', 'D=A', '@temp', 'M=D'])
            else:
                res.extend([f'@{i}', 'D=A', f'@{self._get_label(segment, i)}', 'A=M', 'D=D+A', '@temp', 'M=D'])
            # pop the stack to D
            res.extend(['@SP', 'A=M-1', 'D=M'])
            # Opening the address saved in temp and setting D to it
            res.extend(['@temp', 'A=M', 'M=D'])  
            # Decrement SP
            res.extend(['@SP', 'M=M-1'])

        return res
    
    def _translate_branching_commands(self, instruction):
        res = []
        if instruction[0] == 'label':
            res.extend([f"({instruction[1]})"])
        elif instruction[0] == 'if-goto':
            res.extend(['@SP', 'AM=M-1', 'D=M', f"@{instruction[1]}", 'D;JGT'])
        elif instruction[0] == 'goto':
            res.extend([f'@{instruction[1]}', '0;JMP'])
        
        return res
    
    def translate_instruction(self, instruction):
        instruction = instruction.split()
        if instruction[0] in ['label', 'if-goto', 'goto']:
            return self._translate_branching_commands(instruction)
        elif instruction[0] in ['push', 'pop']:
            return self._translate_memory_commands(instruction)
        elif instruction[0] in ['neg', 'not', 'add', 'sub', 'and', 'or', 'eq', 'gt', 'lt']:
            return self.translate_arthmetic_commands(instruction)
        elif instruction[0] in ['function', 'call', 'return']:
            pass
        else:
            raise KeyError(f'Command not configured: {instruction}')

    def translate(self, instruction_list):
        asm = []

        for instruction in instruction_list:
            print(instruction)
            asm.append(f'\n// {instruction}')
            asm.extend(self.translate_instruction(instruction))

        asm.extend(['(END)', '@END', '0;JMP'])
        return asm
    


# cw = CodeWriter()
# cd = cw.translate([
#     'push constant 7',
#     'push constant 8',
#     'add'
# ])
# print('\n'.join(map(str, cd)))