from JackTokenizer import JackTokenizer
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re

class CompilationEngine:

    tags = {
        'STRING_CONST': 'stringConstant',
        'INT_CONST': 'integerConstant',
        'KEYWORD': 'keyword',
        'SYMBOL': 'symbol',
        'IDENTIFIER': 'identifier',
    }

    def __init__(self, tokenizer: JackTokenizer, outfile=None):
        self.tokenizer = tokenizer
        self.root = None
        self.outfile = outfile
        
    
    def run(self):
        
        if self.tokenizer.currentToken() == 'class':
            self.root = self.compileClass()
        else:
            raise SyntaxError('A Jack file must start with a class declaration.')
        
        rough_string = ET.tostring(self.root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_xml_string = reparsed.documentElement.toprettyxml(indent="  ")
        # Use this in your re.sub() call
        pretty_xml_string = re.sub(r'\n[ \t]*<!-- -->', '', pretty_xml_string)
        


        if self.outfile:
            # Write the formatted XML string to the output file
            with open(self.outfile, 'w') as f:
                f.write(pretty_xml_string)
            
            print(f"Compilation successful! Output written to '{self.outfile}'")
        else:
            # Print the XML to the console as well
            print(pretty_xml_string)

    def _process_element(self, parent_element: ET.Element, expected_type=None, expected_value=None):
        
        token_type = self.tokenizer.tokenType()
        token_value = self.tokenizer.currentToken()

        if expected_type:
            if isinstance(expected_type, list):
                if token_type not in expected_type:
                    raise SyntaxError(f"Expected on of token type {expected_type} but got {token_type} in parent element: {parent_element.tag}\t\t '{token_value}' != '{expected_value}'")
            else:
                if token_type != expected_type:
                    raise SyntaxError(f"Expected token type {expected_type} but got {token_type} in parent element: {parent_element.tag}\t\t '{token_value}' != '{expected_value}'")
            
                
        if expected_value:
            if isinstance(expected_value, list):
                if token_value not in expected_value:
                    raise SyntaxError(f"Expected on of token value '{expected_value}' but got '{token_value}' in parent element: {parent_element.tag}")
            else:
                if token_value != expected_value:
                    raise SyntaxError(f"Expected token value {expected_value} but got {token_value} in parent element: {parent_element.tag}")
                
        

        element = ET.SubElement(parent_element, self.tags[token_type])
        element.text = f' {token_value.strip('\"')} '
        
        self.tokenizer.advance()

        return element

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

    def compileStatements(self):
        statements_element = ET.Element('statements')

        while self.tokenizer.currentToken() in ['let', 'if', 'while', 'do', 'return']:

            if self.tokenizer.currentToken() == 'let':
                statements_element.append(self.compileLet())

            elif self.tokenizer.currentToken() == 'if':
                statements_element.append(self.compileIf())

            elif self.tokenizer.currentToken() == 'while':
                statements_element.append(self.compileWhile())

            elif self.tokenizer.currentToken() == 'do':
                statements_element.append(self.compileDo())

            elif self.tokenizer.currentToken() == 'return':
                statements_element.append(self.compileReturn())

                # If the element has no children, give it empty text to prevent self-closing.
        if not list(statements_element):
            statements_element.append(ET.Comment(" "))


        return statements_element

    def compileLet(self):
        let_element = ET.Element('letStatement')

        self._process_element(let_element, 'KEYWORD', 'let')
        self._process_element(let_element, 'IDENTIFIER')
    
        if self.tokenizer.currentToken() == '[':
            self._process_element(let_element, 'SYMBOL', '[')
            let_element.append(self.compileExpression())
            self._process_element(let_element, 'SYMBOL', ']')

        self._process_element(let_element, 'SYMBOL', '=')
        let_element.append(self.compileExpression())
        self._process_element(let_element, 'SYMBOL', ';')

        return let_element

    def compileIf(self):
        if_element = ET.Element('ifStatement')
        
        self._process_element(if_element, 'KEYWORD', 'if')
        self._process_element(if_element, 'SYMBOL', '(')
        if_element.append(self.compileExpression())
        self._process_element(if_element, 'SYMBOL', ')')
        self._process_element(if_element, 'SYMBOL', '{')
        if_element.append(self.compileStatements())
        self._process_element(if_element, 'SYMBOL', '}')
        if self.tokenizer.currentToken() == 'else':
            self._process_element(if_element, 'KEYWORD', 'else')
            self._process_element(if_element, 'SYMBOL', '{')
            if_element.append(self.compileStatements())
            self._process_element(if_element, 'SYMBOL', '}')

        return if_element

    def compileWhile(self):
        while_element = ET.Element('whileStatement')
        
        self._process_element(while_element, 'KEYWORD', 'while')
        self._process_element(while_element, 'SYMBOL', '(')
        while_element.append(self.compileExpression())
        self._process_element(while_element, 'SYMBOL', ')')
        self._process_element(while_element, 'SYMBOL', '{')
        while_element.append(self.compileStatements())
        self._process_element(while_element, 'SYMBOL', '}')


        return while_element

    def compileDo(self):
        do_element = ET.Element('doStatement')
        self._process_element(do_element, 'KEYWORD', 'do')
        self._compileSubroutineCall(do_element)
        self._process_element(do_element, 'SYMBOL', ';')
        return do_element
    
    def _compileSubroutineCall(self, parent_element):

        self._process_element(parent_element, 'IDENTIFIER')
        if self.tokenizer.currentToken() == '.':
            self._process_element(parent_element, 'SYMBOL', '.')
            self._process_element(parent_element, 'IDENTIFIER')

        self._process_element(parent_element, 'SYMBOL', '(')
        parent_element.append(self.compileExpressionList())
        self._process_element(parent_element, 'SYMBOL', ')')

    def compileReturn(self):
        return_element = ET.Element('returnStatement')

        self._process_element(return_element, 'KEYWORD', 'return')
        if self.tokenizer.currentToken() != ';':
            return_element.append(self.compileExpression())
        self._process_element(return_element, 'SYMBOL', ';')        # ';'

        return return_element

    def compileExpressionList(self):
        expressionList_element = ET.Element('expressionList')
        while self.tokenizer.currentToken() != ')':
            if self.tokenizer.currentToken() == ',':
                self._process_element(expressionList_element, 'SYMBOL', ',')
            expressionList_element.append(self.compileExpression())

        # If the element has no children, give it empty text to prevent self-closing.
        if not list(expressionList_element):
            expressionList_element.append(ET.Comment(" "))

        return expressionList_element

    def compileExpression(self):
        expression_element = ET.Element('expression')

        expression_element.append(self.compileTerm())
        while self.tokenizer.currentToken() in '+-*/&|<>=':
            self._process_element(expression_element, 'SYMBOL')
            expression_element.append(self.compileTerm())
        
        return expression_element
    
    def compileTerm(self):
        """
        Compiles a term. This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routine must distinguish
        between a variable, an array entry, and a subroutine call. A single
        look-ahead token, which may be one of "[", "(", or ".", suffices to distinguish
        between the three possibilities. Any other token is not part of this term and
        should not be advanced over.
        """
        term_element = ET.Element('term')

        token_type = self.tokenizer.tokenType()
        token_value = self.tokenizer.currentToken()

        if token_type in ['INT_CONST', 'STRING_CONST']:
            self._process_element(term_element, token_type)
        elif token_value in ['true', 'false', 'null', 'this']:
            self._process_element(term_element, 'KEYWORD')
        elif token_value in ['~', '-']:
            print(token_value)
            self._process_element(term_element, 'SYMBOL', ['~', '-'])
            term_element.append(self.compileTerm())
        elif token_value == '(':
            self._process_element(term_element, 'SYMBOL', '(')
            term_element.append(self.compileExpression())
            self._process_element(term_element, 'SYMBOL', ')')
        elif token_type == 'IDENTIFIER':
            next_token = self.tokenizer.peek()
            if next_token in ('.', '('):
                self._compileSubroutineCall(term_element)
            else:
                self._process_element(term_element, 'IDENTIFIER') # varName
                if self.tokenizer.currentToken() == '[':
                    self._process_element(term_element, 'SYMBOL', '[')
                    term_element.append(self.compileExpression())
                    self._process_element(term_element, 'SYMBOL', ']')
        else:
            raise SyntaxError(f"Unexpected token in term: {token_value}")

        return term_element


if __name__ == '__main__':
    # Define the input and output file paths
    # IMPORTANT: Update this path to where your Jack file is located.
    input_jack_file = 'D:\\NANDtoTETRIS\\projects\\10\\ArrayTest\\Main.jack'
    output_xml_file = 'Main.xml' # This will be created in the same directory as the script

    try:
        # Read the source Jack code from the input file
        with open(input_jack_file, 'r') as f:
            jack_code = f.read()

        # Initialize the tokenizer and compilation engine
        jt = JackTokenizer(jack_code)
        print(jt.tokens)
        ce = CompilationEngine(jt)

        ce.run()


    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_jack_file}'")
    except SyntaxError as e:
        print(f"A syntax error occurred during compilation: {e}")
