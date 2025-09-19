import os
import glob

from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
from VMWritter import VMWriter

class JackAnalyzer:
    
    def __init__(self, source, destination=None, mode='vm', verbose=0):

        self.mode = mode
        self.destination = destination
        self.verbose = verbose

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
                compilation_engine = CompilationEngine(tokenizer, vm_writer, self.mode, self.verbose)

                if self.verbose >= 1:
                    print('-'*88)
                    print(jackfile)
                    print()

                # out is xml or vm based on the mode. print according to the output arg
                out = compilation_engine.compile()

                if self.destination:
                    path, filename = os.path.split(jackfile)
                    basename, extension = os.path.splitext(filename)
                    output_filename = basename + f'.{self.mode}'

                    if os.path.isdir(self.destination):
                        with open(os.path.join(self.destination, output_filename), 'w') as f:
                            f.write(out)
                    else:
                        raise ValueError('Destination must be stdout or a directory!')



import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input', 
        type=str, 
        help='The input directory or file to process'
        )
    
    parser.add_argument(
        '--output', 
        type=str, 
        default=None,
        help='An optional string argument that defaults to None'
        )
    
    parser.add_argument(
        '-m', '--mode', 
        type=str, 
        choices=['vm', 'xml'], 
        default='vm',
        help='Generates the respective code based on the flag.'
        )
    
    parser.add_argument(
        '-v', '--verbose',
        action='count', 
        default=0,
        help='Increase output verbosity. Can be used up to three times (-v, -vv, -vvv).'
        )
    
    args = parser.parse_args()


    jack_analyzer = JackAnalyzer(args.input, args.output, args.mode, args.verbose)

