from SymbolManager import SymbolManager

'''
Takes in the assembly code and parse it into different parts of the code
receives lines of code after preprocessing from MainIO
'''
class Parser:

    def __init__(self, symbol_manager):
        self.symbol_manager = symbol_manager
        pass                

    ''' Returns a tuple of signature: (type('A', 'C'), values)
        A instruction values: the digits that follwo the @
        C instruction values: (comp, dest, jump (default = null)) // use the table from the lecture
    '''
    def parse(self, lines):
        parsed_tuples = []
        
        for line in lines:
            is_countable = False
            line = line.strip()
            if line[0] == '@':
                # A instruction
                is_countable = True
                instruction_type = 'A'
                values = line[1:]
            elif line[0] == '(':
                symbol = line[1:-1]
                self.symbol_manager.add(symbol, len(parsed_tuples))
            else:
                # C instruction
                is_countable = True
                instruction_type = 'C'
                line = '#' + line + '#'

                idx_eq = line.find('=')
                idx_eq = 0 if idx_eq == -1 else idx_eq
                idx_semi = line.find(';')
                idx_semi = len(line) - 1 if idx_semi == -1 else idx_semi

                dest = line[1:idx_eq]
                comp = line[idx_eq + 1:idx_semi]
                jump = line[idx_semi + 1:-1]

                values = tuple((dest, comp, jump))
            if is_countable:
                parsed_tuples.append(tuple((instruction_type, values)))

        return parsed_tuples
    

# p = Parser()
# for line in p.clean('@21 \n D;JGE // ksdjf \n A=A+D;JMP'):
#     print(p.parse(line))