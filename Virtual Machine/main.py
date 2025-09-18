import sys
from parser import Parser

# File validation
filepath = sys.argv[1]
if filepath.split('.')[-1] != 'vm':
    print('Provide a valid .vm file')
    exit()

parser  = Parser()

vmcode = ''
with open(filepath, 'r') as f:
    vmcode = f.read()
    code_list = parser.parse(vmcode)
    
    print(code_list)
    


