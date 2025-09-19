
class SymbolTable:

    def __init__(self, name=None):
        self.class_name = name
        self.class_scope = {}
        self.subroutine_signatures = {}
        self.class_index_counter = 0

        self.subroutine_name = None
        self.subroutine_type = None
        self.subroutine_scope = {}
        self.subroutine_label_counter = 0
        
        self.index_counters = {'static': 0, 'field': 0,'var': 0, 'arg': 0}
          
    def startSubroutine(self, name):

        # print(f'Subroutine name: {self.subroutine_name}')
        # print(f'Subroutine scope')
        # for item in self.subroutine_scope.items():
        #     print(item)
        # print()

        self.subroutine_name = name
        self.subroutine_scope = {}
        self.subroutine_label_counter = 0
        self.index_counters['var'] = 0
        self.index_counters['arg'] = 0

    def define_signature(self, name, kind, type, nArgs, nLocals):
        entry = {'kind': kind, 'type': type, 'nArgs': nArgs, 'nLocals': nLocals}

        if name in self.subroutine_signatures:
            raise ValueError(f'Subroutine {name} defined more than once')
        
        self.subroutine_signatures[name] = entry

    def getnLocals(self, name):
        if name in self.subroutine_signatures:
            return self.subroutine_signatures[name]['nLocals']
        else:
            print(self.subroutine_signatures)
            raise ValueError(f'Subroutine: "{name}" not found in subroutine signatures')
        
    def define(self, name, type, kind):
        entry = {'kind': kind, 'type': type, 'index': None}

        if entry['kind'] in ['static','field']:
            entry['index'] = self.class_index_counter
            self.class_index_counter += 1

            if name in self.class_scope:
                raise ValueError(f'Symbol defined more that once in the class scope: {name}')

            self.class_scope[name] = entry
        elif entry['kind'] in ['var', 'arg']:
            entry['index'] = self.index_counters[entry['kind']]
            self.index_counters[entry['kind']] += 1

            if name in self.subroutine_scope:
                raise ValueError(f'Symbol defined more that once in the subroutine scope: {name}')
    
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
        elif name in self.subroutine_signatures:
            return self.subroutine_signatures[name]['type']
        else:
            raise KeyError(f'Variable not found in symbol table: {name}') 

    def kindOf(self, name):
        if name in self.subroutine_scope:
            return self.subroutine_scope[name]['kind']
        elif name in self.class_scope:
            return self.class_scope[name]['kind']
        else:
            print('Class scope: ', self.class_scope)
            print('Subroutine scope', self.subroutine_scope)
            raise KeyError(f"Variable not found in symbol table: {name}")  

    def _getBaseLabel(self, labels=None):
        base_label = f"{self.class_name}.{self.subroutine_name}.{self.subroutine_label_counter}"
        self.subroutine_label_counter += 1

        if labels:
            labels = tuple(map(lambda x: f'{base_label}.{x}', labels))
            return labels

        return base_label




    


