import os
import sys
from .parser import Parser
from .codewriter import CodeWriter



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
        codew = CodeWriter()
        for vmfile in target_files:
            filename = os.path.splitext(os.path.basename(vmfile))[0]
            with open(vmfile, 'r') as f:
                vmcode = self.parser.parse(f.read())
                asmcode = codew.translate(vmcode, filename)
                if os.path.basename(vmfile) == 'Sys.vm':
                    final_asmcode = asmcode + final_asmcode
                else:
                    final_asmcode.extend(asmcode)

        # Prepend the bootstrap code such as setting SP and the initial frame
        final_asmcode = codew.get_bootstrap() + final_asmcode
        
        final_asmcode = '\n'.join(final_asmcode)

        asmfile = os.path.splitext(os.path.basename(target))[0] + '.asm'
        if self.dest_dir:
            asmfile = os.path.join(self.dest_dir, asmfile)
        with open(asmfile, 'w') as f:
            f.write(final_asmcode)


if __name__ == "__main__":
    vmt = VMTranslator()
    vmt.run(sys.argv[1])