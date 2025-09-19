from JackTokenizer import JackTokenizer


class CompilationEngine:

    def __init__(self, tokenizer: JackTokenizer):
        self.jt = tokenizer

    def run(self):
        while self.jt.hasMoreTokens:
            print(self.jt.currentToken())
            self.jt.advance()

    def compileClass(self):
        pass


