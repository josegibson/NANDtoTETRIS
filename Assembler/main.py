from Parser import Parser
from SymbolManager import SymbolManager
from Convert import Convert

import sys

def clean(fullcode):
    cleaned_lines = []
    for line in fullcode.split('\n'):

        idx_cmt = line.find('//')
        if idx_cmt != -1:
            line = line[:idx_cmt]

        if len(line.strip()) == 0:
            continue
        
        cleaned_lines.append(line.strip())
    
    return cleaned_lines

symbol_mgr = SymbolManager()
parser = Parser(symbol_mgr)
converter = Convert(symbol_mgr)

machine_code = ''

filepth = sys.argv[1]

with open(filepth, 'r') as f:
    fullcode = f.read()
    clean_lines = clean(fullcode)
    # Firstpass happens here where the loop symbols are recorded but variable symbols are not
    parsed_tuples = parser.parse(clean_lines)
    # print(parsed_tuples)
    # symbol_mgr.print()

    final_asm = converter.replace_symbols(parsed_tuples)
    # print(final_asm)
    # symbol_mgr.print()

    machine_code = converter.convert_binary(final_asm)
    # print("\n".join(machine_code))

output_file = filepth.split('.')[0] + '.hack'
with open(output_file, 'w', newline='\n') as f:
    for instruction in machine_code:
        f.write(instruction.strip() + '\n')

