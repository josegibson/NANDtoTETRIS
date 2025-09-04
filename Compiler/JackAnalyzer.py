import os
import glob

from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
from VMWritter import VMWriter

class JackAnalyzer:
    
    def __init__(self, source, destination, mode='vm'):

        self.mode = mode
        self.destination = destination

        self.jackfiles = []
        self.source = source
        if os.path.isdir(source):
            self.jackfiles.extend(glob.glob(os.path.join(source, "*.jack")))
        else:
            self.jackfiles.extend([source])

        self.analyze()

    def analyze(self):
        for jackfile in self.jackfiles:
            with open(jackfile, 'r') as f:
                jackcode = f.read()
                tokenizer = JackTokenizer(jackcode)
                vm_writer = VMWriter()
                compilation_engine = CompilationEngine(tokenizer, vm_writer, self.mode)

                # compilation_engine.symbol_table.define_signature('Output.println', 'function', 'void', 1, None)
                # compilation_engine.symbol_table.define_signature('Output.printInt', 'function', 'void', 1, None)
                # compilation_engine.symbol_table.define_signature('Memory.peek', 'function', 'int', 1, None)
                # compilation_engine.symbol_table.define_signature('Memory.poke', 'function', 'void', 2, None)
                
                # out is xml or vm based on the mode. print according to the output arg
                out = compilation_engine.compile()

                path, filename = os.path.split(jackfile)
                basename, extension = os.path.splitext(filename)
                outfile = basename + f'.{self.mode}'

                if self.destination == 'stdout':
                    print('\n', '-'*100, '\n')
                    print(outfile)
                    print('\n\t' + out.replace('\n', '\n\t'))
                    print('\n', '-'*100, '\n')
                else:
                    if os.path.isdir(self.destination):
                        with open(os.path.join(self.destination, outfile)) as f:
                            f.write(out)
                    else:
                        raise ValueError('Destination must be a directory!')



import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str)
    parser.add_argument('--output', type=str, default='stdout')
    parser.add_argument('--mode', type=str, choices=['vm', 'xml'], default='vm')
    args = parser.parse_args()


    jack_analyzer = JackAnalyzer(args.input, args.output, args.mode)

