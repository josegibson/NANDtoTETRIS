import os
import sys
from parser import Parser
from codewriter import CodeWriter



class VMTranslator:
    def __init__(self):
        self.parser = Parser()

    def file_validation(self, filepath):
        if filepath.split('\\')[-1].split('.')[-1] != 'vm':
            print('Provide a valid .vm file')
            exit()

    def translate(self, filepath, outdir=None):
        # Passing static file to name static labels
        filename = os.path.basename(filepath)
        cw = CodeWriter(filename=os.path.splitext(filename)[0])

        asmcode = ''
        with open(filepath, 'r') as f:
            vmcode = f.read()
            code_list = self.parser.parse(vmcode)
            final_asm = cw.translate(code_list)
            asmcode = '\n'.join(map(str, final_asm))


        outfile = os.path.splitext(filename)[0] + '.asm'
        if outdir != None:
            outfile = os.path.join(outdir, outfile)
        
        with open(outfile, 'w') as f:
            f.write(asmcode)
    


if __name__ == "__main__":
    vmt = VMTranslator()
    vmt.translate(sys.argv[1])