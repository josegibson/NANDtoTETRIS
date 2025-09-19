
class SymbolTable:

    def __init__(self, name):
        self.class_name = name
        self.subroutine_name = None

        self.subroutine_scope = {}
        self.class_scope = {}
        self.index_counters = {'static': 0, 'field': 0,'var': 0, 'arg': 0}
        self.class_counter = 0
        self.subroutine_counter = 0

    def startSubroutine(self, name):
        self.subroutine_name = name
        self.subroutine_scope = {}
        self.subroutine_counter = 0
        self.index_counters = {'static': 0, 'field': 0,'var': 0, 'arg': 0}

    def define(self, name, type, kind):
        entry = {'kind': kind, 'type': type, 'index': self.counter}
        self.counter += 1
        self.index_counters[entry['kind']] += 1

        if entry['kind'] in ['static','field']:
            self.class_scope[name] = entry
        elif entry['kind'] in ['var', 'arg']:
            self.subroutine_scope[name] = entry
        else:
            raise KeyError(f"Invalid kind; variable '{name}' has an invalid kind: '{entry['kind']}'")
        
    def varCount(self, kind):
        return self.index_counters[kind]
    
    def indexOf(self, name):
        if name in self.subroutine_scope:
            return self.subroutine_scope[name]['index']
        elif name in self.class_scope:
            return self.class_scope[name]['index']
        else:
            raise KeyError(f'Variable not found in symbol table: {name}')
        
    def typeOf(self, name):
        if name in self.subroutine_scope:
            return self.subroutine_scope[name]['type']
        elif name in self.class_scope:
            return self.class_scope[name]['type']
        else:
            raise KeyError(f'Variable not found in symbol table: {name}') 

    def kindOf(self, name):
        if name in self.subroutine_scope:
            return self.subroutine_scope[name]['kind']
        elif name in self.class_scope:
            return self.class_scope[name]['kind']
        else:
            raise KeyError(f'Variable not found in symbol table: {name}')  





    


