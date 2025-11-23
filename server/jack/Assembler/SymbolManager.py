
predefined_symbols = {
    'R0': 0,
    'R1': 1,
    'R2': 2,    
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,    
    'R15': 15,
    'SCREEN': 16384,
    'KBD' : 24576,
    'SP' : 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4
}

class SymbolManager():
    def __init__(self):
        self.predefined_symbols_dict = predefined_symbols
        self.symbol_table = {}
        self.memory_index = 16

    def fetch(self, symbol):
        if symbol in predefined_symbols:
            return predefined_symbols[symbol]
        if symbol in self.symbol_table:
            return self.symbol_table[symbol]
    
        return self.add(symbol)
        
        
    def add(self, symbol, value=None):
        if value is None:
            value = self.memory_index
            self.memory_index += 1
        self.symbol_table[symbol] = value
        return value
        
    def decode(self, value):
        if value.isdigit():
            return int(value)
        else:
            return self.fetch(value)
        
    def print(self):
        print("Predefined symbol Table")
        print(self.predefined_symbols_dict)
        print()
        print("Symbol Table")
        print(self.symbol_table)
        print()