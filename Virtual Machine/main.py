import sys
from parser import Parser
from codewriter import CodeWriter

# File validation
filepath = sys.argv[1]
print(filepath.split('.'))
if filepath.split('.')[-1] != 'vm':
    print('Provide a valid .vm file')
    exit()

parser  = Parser()
cw = CodeWriter()

vmcode = ''
asmcode = ''
with open(filepath, 'r') as f:
    vmcode = f.read()
    code_list = parser.parse(vmcode)
    final_asm = cw.translate(code_list)
    asmcode = '\n'.join(map(str, final_asm))

outfile = filepath.split('.')[0] + '.asm'
with open(outfile, 'w') as f:
    f.write(asmcode)
    


