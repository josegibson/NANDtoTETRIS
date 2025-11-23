from .Parser import Parser
from .SymbolManager import SymbolManager
from .Convert import Convert

import sys


def clean(fullcode):
    """Transforms astring of code into a list of assembly instructions,
    omitting blank lines and comments."""
    cleaned_lines = []
    for line in fullcode.split('\n'):

        idx_cmt = line.find('//')
        if idx_cmt != -1:
            line = line[:idx_cmt]

        if len(line.strip()) == 0:
            continue
        
        cleaned_lines.append(line.strip())
    
    return cleaned_lines


def assemble_file(filepth):
    """Assemble a .asm file to .hack binary format.
    
    Args:
        filepth: Path to the .asm file
        
    Returns:
        Path to the generated .hack file
    """
    symbol_mgr = SymbolManager()
    parser = Parser(symbol_mgr)
    converter = Convert(symbol_mgr)

    with open(filepth, 'r') as f:
        fullcode = f.read()
        clean_lines = clean(fullcode)
        # Firstpass happens here where the loop symbols are recorded but variable symbols are not
        parsed_tuples = parser.parse(clean_lines)

        final_asm = converter.replace_symbols(parsed_tuples)

        machine_code = converter.convert_binary(final_asm)

    output_file = filepth.split('.')[0] + '.hack'
    with open(output_file, 'w', newline='\n') as f:
        for instruction in machine_code:
            f.write(instruction.strip() + '\n')
    
    return output_file


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python main.py <file.asm>")
        sys.exit(1)
    
    assemble_file(sys.argv[1])
