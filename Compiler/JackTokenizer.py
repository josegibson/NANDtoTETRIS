import re


class JackTokenizer:
    KEYWORDS = ['class', 'method', 'int', 'false', 'if', 'function', 'static', 'boolean', 'this', 'while', 'constructor', 'field', 'char', 'null', 'else', 'true', 'var', 'void', 'let', 'do', 'return']
    SYMBOLS = set('~{}()[].,;+-*/&|<>=`')

    def __init__(self, jackcode):

        code = re.sub(r"//.*$", "", jackcode, flags=re.MULTILINE)
        code = re.sub(r"/\*\*.*?\*/", "", code, flags=re.DOTALL)

        token_pattern = r"\".*?\"|\d+|[_a-zA-Z]\w*|[{}\(\)\[\].,;+\-*/&|<>=~`]"
        self.tokens = re.findall(token_pattern, code)

        self.tokenslen = len(self.tokens)
        self.curr = 0

    def hasMoreTokens(self):
        return self.curr < self.tokenslen
    
    def advance(self):
        self.curr += 1

    def currentToken(self):
        if self.hasMoreTokens():
            return self.tokens[self.curr]
        else:
            print(self.tokenslen, self.curr)
            raise KeyError
        
    def peek(self):
        if self.curr + 1 < self.tokenslen:
            return self.tokens[self.curr + 1]
        else:
            raise KeyError    
    def tokenType(self):
        currtoken = self.tokens[self.curr]

        if currtoken in self.KEYWORDS:
            return 'KEYWORD'
        elif currtoken in self.SYMBOLS:
            return 'SYMBOL'
        elif re.match(r"\d+", currtoken):
            return 'INT_CONST'
        elif re.match(r"^\".*?\"$", currtoken):
            return 'STRING_CONST'
        elif re.match(r"^[_a-zA-Z]*.*?$", currtoken):
            return 'IDENTIFIER'
        else:
            raise KeyError
        
    def keyword(self):
        return self.currentToken if self.tokenType == 'KEYWORD' else None
    
    def symbol(self):
        return self.currentToken if self.tokenType == 'SYMBOL' else None
    
    def stringVal(self):
        return self.currentToken if self.tokenType == 'STRING_CONST' else None
    
    def intVal(self):
        return self.currentToken if self.tokenType == 'INT_CONST' else None
    
    def identifier(self):
        return self.currentToken if self.tokenType == 'INDENTIFIER' else None
    



if __name__ == '__main__':
    test_jack_code = """
    // trsdyfguhijok yrtdyfguhb ytuguhre $*^&GYUIBV FT&%D
    
    class TokenTest {
        field int myVar;
        static boolean _flag;

        constructor TokenTest new() {
            let myVar = 1234;
            let _flag = true;
            do Output.printString("hello world");
            return this;
        }

        method void testSymbols() {
            var int a, b;
            let a = (1 + 2) * 3;
            let b = a - 4 / 5;
            if (a < b & a > 0) {
                do Output.printInt(a);
            } else {
                do Output.printInt(b);
            }
            return;
        }
    }"""

    jt = JackTokenizer(test_jack_code)
    
    
    while jt.hasMoreTokens():
        print(jt.tokenType(), jt.currentToken())
        jt.advance()
