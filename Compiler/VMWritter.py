class VMWriter:
    def __init__(self, vm_out_path=None):
        self.vmcode = []
    
    def writeComment(self, comment, begin='\n', end = ''):
        self.vmcode.append(f"{begin}// {comment} {end}")

    def writePush(self, segemnt: str, index: int):
        self.vmcode.append(f'push {segemnt} {index}')

    def writePop(self, segemnt: str, index: int):
        self.vmcode.append(f'pop {segemnt} {index}')

    def writeArthmetic(self, command: str):
        command_dict = {
            '+' : 'add',
            '-' : 'sub',
            '&' : 'and',
            '|' : 'or',
            '=' : 'eq',
            '<' : 'lt',
            '>' : 'gt'
        }

        command_dict_v2 = {
            'NOT': 'not',
            'NEG': 'neg'
        }

        if command in command_dict:
            self.vmcode.append(command_dict[command])
        elif command in command_dict_v2:
            self.vmcode.append(command_dict_v2[command])
        else:
            if command == '*':
                self.writeCall('Math.multiply', 2)
            elif command == '/':
                self.writeCall('Math.divide', 2)

    def writeFunction(self, name: str, nLocals: int):
        self.vmcode.append(f'function {name} {nLocals}')

    def writeCall(self, name: str, nArgs: int):
        self.vmcode.append(f'call {name} {nArgs}')

    def writeReturn(self):
        self.vmcode.append(f'return')

    def writeLabel(self, label):
        self.vmcode.append(f"label {label}")

    def writeGoto(self, label):
        self.vmcode.append(f"goto {label}")

    def writeIf(self, label):
        self.vmcode.append(f"if-goto {label}")



        
        


    

    

    



    
