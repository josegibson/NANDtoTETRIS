import os
import sys
from parser import Parser
from codewriter import CodeWriter



class VMTranslator:
    def __init__(self, dest_dir=None):
        self.parser = Parser()
        self.dest_dir = dest_dir

    def run(self, target):

        target_files = []

        # Adding relevant files to target_files
        if os.path.isdir(target):
            target_files.extend([os.path.join(target, i) for i in os.listdir(target)])
        elif os.path.isfile(target):
            target_files.append(target)

        # Filtering to keep only the .vm files
        target_files = [file for file in target_files if os.path.splitext(os.path.basename(file))[-1] == '.vm']

        if len(target_files) == 0:
            raise ValueError('No valid .vm file found')
        
        
        final_asmcode = []

        for vmfile in target_files:
            codew = CodeWriter(os.path.splitext(os.path.basename(vmfile))[0])
            with open(vmfile, 'r') as f:
                vmcode = self.parser.parse(f.read())
                asmcode = codew.translate(vmcode)
                if os.path.basename(vmfile) == 'Sys.vm':
                    final_asmcode = asmcode + final_asmcode
                else:
                    final_asmcode.append(asmcode)

        
        final_asmcode = '/n'.join(final_asmcode)

        asmfile = os.path.splitext(os.path.basename(target))[0] + '.asm'
        if self.dest_dir:
            asmfile = os.path.join(self.dest_dir, asmfile)
        with open(asmfile, 'w') as f:
            f.write(final_asmcode)



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
    vmt.run(sys.argv[1])