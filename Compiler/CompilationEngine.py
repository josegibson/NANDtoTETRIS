from JackTokenizer import JackTokenizer


class CompilationEngine:

    def __init__(self, tokenizer: JackTokenizer):
        self.jt = tokenizer

    def run(self):
        while self.jt.hasMoreTokens:
            print(self.jt.currentToken())
            self.jt.advance()

    def compileClass(self):
        class_element = ET.Element('class')
        
        self._process_element(class_element, 'KEYWORD', 'class')
        self._process_element(class_element, 'IDENTIFIER')
        self._process_element(class_element, 'SYMBOL', '{')

        while self.tokenizer.currentToken() in ['static', 'field', 'constructor', 'method', 'function']:

            if self.tokenizer.currentToken() in ['static', 'field']:
                class_element.append(self.compileClassVarDec())

            if self.tokenizer.currentToken() in ['constructor', 'method', 'function']:
                class_element.append(self.compileSubroutine())

        self._process_element(class_element, 'SYMBOL', '}')

        return class_element
    
    def compileClassVarDec(self):
        classVarDec_element = ET.Element('classVarDec')

        self._process_element(classVarDec_element, 'KEYWORD', ['static', 'field'])
        self._process_element(classVarDec_element, ['KEYWORD', 'IDENTIFIER'])
        self._process_element(classVarDec_element,'IDENTIFIER')
        while self.tokenizer.currentToken() == ',':
            self._process_element(classVarDec_element,'SYMBOL', ',')
            self._process_element(classVarDec_element,'IDENTIFIER')

        self._process_element(classVarDec_element,'SYMBOL', ';')

        return classVarDec_element
        
    def compileParameterList(self):
        parameterList_element = ET.Element('parameterList')

        while self.tokenizer.currentToken() != ')':

            if(self.tokenizer.currentToken() == ','):
                self._process_element(parameterList_element, 'SYMBOL', ',')
            self._process_element(parameterList_element, ['KEYWORD', 'IDENTIFIER'])
            self._process_element(parameterList_element, 'IDENTIFIER')
        
        # If the element has no children, give it empty text to prevent self-closing.
        if not list(parameterList_element):
            parameterList_element.append(ET.Comment(" "))


        return parameterList_element

    def compileSubroutine(self):
        subroutine_element = ET.Element('subroutineDec')

        self._process_element(subroutine_element, 'KEYWORD', ['constructor', 'function', 'method'])
        self._process_element(subroutine_element, ['KEYWORD', 'IDENTIFIER'])
        self._process_element(subroutine_element, 'IDENTIFIER')    #subroutineName
        self._process_element(subroutine_element, 'SYMBOL', '(')
        subroutine_element.append(self.compileParameterList())
        self._process_element(subroutine_element, 'SYMBOL', ')')

        # subroutineBody
        subroutineBody_element = ET.Element('subroutineBody')
        
        self._process_element(subroutineBody_element, 'SYMBOL', '{')
        while self.tokenizer.currentToken() == 'var':
            subroutineBody_element.append(self.compileVarDec())
        subroutineBody_element.append(self.compileStatements())
        self._process_element(subroutineBody_element, 'SYMBOL', '}')

        subroutine_element.append(subroutineBody_element)

        return subroutine_element
    
    def compileVarDec(self):
        varDec_element = ET.Element('varDec')

        self._process_element(varDec_element, 'KEYWORD', 'var')
        self._process_element(varDec_element, ['KEYWORD', 'IDENTIFIER'])
        self._process_element(varDec_element, 'IDENTIFIER')

        while self.tokenizer.currentToken() != ';':
            self._process_element(varDec_element, 'SYMBOL', ',')

            self._process_element(varDec_element, 'IDENTIFIER')
        self._process_element(varDec_element, 'SYMBOL', ';')

        return varDec_element
