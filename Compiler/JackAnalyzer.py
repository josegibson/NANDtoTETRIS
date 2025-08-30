import os
import glob
import sys

from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
from VMWritter import VMWriter
from SymbolTable import SymbolTable

class JackAnalyzer:
    
    def __init__(self, source, destination=None):
        self.jackfiles = []
        self.source = source
        self.destination = destination if destination else self.source
        if os.path.isdir(source):
            self.jackfiles.extend(glob.glob(os.path.join(source, "*.jack")))
        else:
            self.jackfiles.extend([source])

        self.compile()

    def compile(self):
        for jackfile in self.jackfiles:
            xmlpath = os.path.join(self.destination, f'{os.path.splitext(os.path.basename(jackfile))[0]}.xml')

            with open(jackfile, 'r') as f:
                jackcode = f.read()
                jt = JackTokenizer(jackcode)
                vw = VMWriter()
                st = SymbolTable()
                ce = CompilationEngine(jt, vw, xmlpath)
                ce.run()


if __name__ == '__main__':
    output_path = None
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    ja = JackAnalyzer(sys.argv[1], output_path)

