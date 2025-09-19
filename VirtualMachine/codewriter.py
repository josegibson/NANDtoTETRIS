

class CodeWriter():
    def __init__(self, filename):
        self.label_id = 0
        self.filename = filename

        self.label = {
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT',
            ('pointer', '0'): 'THIS',
            ('pointer', '1'): 'THAT',
            'temp': '5' 
        }

        # function : seed
        self.function_seed = 0

    def _get_label(self, segment_id, i):
        
        if segment_id == 'static':
            return f"{self.filename}.{i}"
        elif segment_id == 'pointer':
            return self.label[(segment_id, i)]
        else:
            return self.label[segment_id]
        
    def _translate_arthmetic_commands(self, instruction):
        op = instruction[0]
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
                res.extend(['D=M-D'])

                if op == 'eq':
                    res.extend([f'@{self.filename}_TRUE_{self.label_id}', 'D;JEQ'])
                elif op == 'gt':
                    res.extend([f'@{self.filename}_TRUE_{self.label_id}', 'D;JGT'])
                elif op == 'lt':
                    res.extend([f'@{self.filename}_TRUE_{self.label_id}', 'D;JLT'])
                
                # Setup TRUE, FALSE and CONTINUE labels
                res.extend(['@SP', 'A=M', 'M=0', f'@{self.filename}_END_{self.label_id}', '0;JMP'])
                res.extend([f'({self.filename}_TRUE_{self.label_id})', '@SP', 'A=M', 'M=-1'])
                res.extend([f'({self.filename}_END_{self.label_id})'])
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
                res.extend([f'@{i}', 'D=A', f'@{self._get_label(segment, i)}', 'D=D+M', '@R13', 'M=D'])
            # pop the stack to D
            res.extend(['@SP', 'A=M-1', 'D=M'])
            # Opening the address saved in temp and setting D to it
            res.extend(['@R13', 'A=M', 'M=D'])  
            # Decrement SP
            res.extend(['@SP', 'M=M-1'])

        return res
    
    def _translate_branching_commands(self, instruction):
        res = []
        if instruction[0] == 'label':
            res.extend([f"({instruction[1]})"])
        elif instruction[0] == 'if-goto':
            res.extend(['@SP', 'AM=M-1', 'D=M', f"@{instruction[1]}", 'D;JNE'])
        elif instruction[0] == 'goto':
            res.extend([f'@{instruction[1]}', '0;JMP'])
        return res

    def _translate_function_commands(self, instruction):
        res = []
        if instruction[0] == 'function':
            # Add to the function map, along with the local variables requirements
            self.function_map[instruction[1]] = instruction[2]
            self.function_seed[instruction[1]] = 0

            # Add (function name) to the asm command (filename already included int the functioname in vmcode)
            res.extend([f'({instruction[1]})'])

            # Setting up the local variabels to 0
            res.extend(['@0', 'D=A'])
            for i in range(instruction[2]):
                res.extend(['@SP', 'A=M', 'M=D', '@SP', 'M=M+1'])

        elif instruction[0] == 'call':
            # Create a label for the return address
            retAddr = f'RETURN_{self.filename}_{self.function_seed}'
            self.function_seed += 1


            # Save the current frame
            res.extend([f'@{retAddr}', 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']) # Save the return address and increment SP
            res.extend(['@LCL', 'D=M', '@SP', 'A=M','M=D', '@SP', 'M=M+1']) # Save LCL and increment
            res.extend(['@ARG', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']) # Save ARG and increment
            res.extend(['@THIS', 'D=M', '@SP', 'A=M','M=D', '@SP', 'M=M+1']) # Save THIS and increment
            res.extend(['@THAT', 'D=M', '@SP', 'A=M','M=D', '@SP', 'M=M+1']) # Save THAT and increment

            # Set the frame for this current function
            res.extend(['@5', 'D=A', '@SP', 'D=M-D', f'@{instruction[2]}', 'D=D-A', '@ARG', 'M=D']) # Setup the ARG since it is equal *SP-5-nArgs
            res.extend(['@SP', 'D=M', '@LCL', 'M=D']) # Setup LCL since it is equal to *SP
            
            # Not defining THIS or THAT, this is required only for a constructor function

            # # Set up the local variables required using lookup
            # res.extend(['@0', 'D=A', '@SP', 'A=M'])
            # for i in range(self.function_map[instruction[1]]):
            #     res.extend(['M=D', 'A=A+1', '@SP', 'M=M+1']) # Set 0 and increment SP. Note: D = 0

            # Do @function label and jump
            res.extend([f'@{instruction[1]}', '0;JMP'])
            res.extend([f'({retAddr})'])

        elif instruction[0] == 'return':
            # Restore the frame
            # exepcted return value at *ARG

            # frame = LCL
            res.extend(['@LCL', 'D=M', '@R13', 'M=D'])

            # ret = *(frame - 5)
            res.extend(['@5', 'D=A', '@R13', 'D=M-D', 'A=D', 'D=M', '@R14', 'M=D'])

            # *ARG = pop()
            res.extend(['@SP', 'AM=M-1', 'D=M', '@ARG', 'A=M', 'M=D'])

            # SP = ARG + 1
            res.extend(['@ARG', 'D=M+1', '@SP', 'M=D'])

            # THAT  = *(frame - 1)
            res.extend(['@1', 'D=A', '@R13', 'D=M-D', 'A=D', 'D=M', '@THAT', 'M=D'])

            # THIS  = *(frame - 2)
            res.extend(['@2', 'D=A', '@R13', 'D=M-D', 'A=D', 'D=M', '@THIS', 'M=D'])

            # ARG = *(frame - 3)
            res.extend(['@3', 'D=A', '@R13', 'D=M-D', 'A=D', 'D=M', '@ARG', 'M=D'])

            # LCL = *(frame - 4)
            res.extend(['@4', 'D=A', '@R13', 'D=M-D', 'A=D', 'D=M', '@LCL', 'M=D'])

            # goto ret
            res.extend(['@R14', 'A=M', '0;JMP'])

        return res
    
    def translate_instruction(self, instruction):
        instruction = instruction.split()
        if instruction[0] in ['label', 'if-goto', 'goto']:
            return self._translate_branching_commands(instruction)
        elif instruction[0] in ['push', 'pop']:
            return self._translate_memory_commands(instruction)
        elif instruction[0] in ['neg', 'not', 'add', 'sub', 'and', 'or', 'eq', 'gt', 'lt']:
            return self._translate_arthmetic_commands(instruction)
        elif instruction[0] in ['function', 'call', 'return']:
            return self._translate_function_commands(instruction)
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
    

if __name__ == "__main__":
    cw = CodeWriter()
    cd = cw.translate([
        'push constant 7',
        'push constant 8',
        'add'
    ])
    print('\n'.join(map(str, cd)))