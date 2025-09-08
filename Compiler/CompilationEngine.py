from JackTokenizer import JackTokenizer
from VMWritter import VMWriter
from SymbolTable import SymbolTable

import xml.etree.ElementTree as ET
from xml.dom import minidom
import re

class CompilationEngine:

    def __init__(self, tokenizer: JackTokenizer, vWriter: VMWriter, mode='vm', verbose=True):

        self.mode = mode
        self.verbose = verbose

        self.tokenizer = tokenizer
        self.root = None
        self.vmWriter = vWriter
        self.symbol_table = SymbolTable()

        # a buffer to record the processed tokens, this can be useful for testing
        self.jackcode_buffer = []

    @staticmethod
    def comment(funct):
        def wrapped(self, *args,**kwargs):
            self.vmWriter.writeComment('')
            self.processed_buffer.clear()

            result = funct(self, *args, **kwargs)

            self.vmWriter.writeComment(" ".join(self.processed_buffer), begin='', end='\n')
            self.processed_buffer.clear()

            return result

        return wrapped

    def _buildSymbolTable(self):
        
        while self.tokenizer.hasMoreTokens():
            if self.tokenizer.peekCurrentToken() == 'class':
                # Skip the class keyword
                self.tokenizer.advance()    
                self.symbol_table.class_name = self.tokenizer.peekCurrentToken()
            elif self.tokenizer.peekCurrentToken() in ['static', 'field']:
                kind = self.tokenizer.peekCurrentToken()
                self.tokenizer.advance()

                type = self.tokenizer.peekCurrentToken()
                self.tokenizer.advance()

                name = self.tokenizer.peekCurrentToken()
                self.tokenizer.advance()

                self.symbol_table.define(name, type, kind)

                while self.tokenizer.peekCurrentToken() == ',':
                    # Skip the ','
                    self.tokenizer.advance()

                    name = self.tokenizer.peekCurrentToken()
                    self.tokenizer.advance()

                    self.symbol_table.define(name, type, kind)

            elif self.tokenizer.peekCurrentToken() in ['constructor', 'function', 'method']:
                subroutine_kind = self.tokenizer.peekCurrentToken()
                self.tokenizer.advance()

                subroutine_type = self.tokenizer.peekCurrentToken()
                self.tokenizer.advance()

                subroutine_name = self.tokenizer.peekCurrentToken()
                self.tokenizer.advance()

                self.symbol_table.startSubroutine(subroutine_name)

                nArgs = 0
                self.tokenizer.advance()    # (
                while self.tokenizer.peekCurrentToken() != ')':
                    arg_kind = self.tokenizer.peekCurrentToken()
                    self.tokenizer.advance()

                    arg_name = self.tokenizer.peekCurrentToken()
                    self.tokenizer.advance()

                    nArgs += 1
                    self.symbol_table.define(arg_name, arg_kind, 'arg')

                    if self.tokenizer.peekCurrentToken() == ',':
                        self.tokenizer.advance()

                self.tokenizer.advance()    # )

                self.tokenizer.advance()    # {
                nLocals = 0
                while self.tokenizer.peekCurrentToken() == 'var':
                    kind = self.tokenizer.peekCurrentToken()
                    self.tokenizer.advance()

                    type = self.tokenizer.peekCurrentToken()
                    self.tokenizer.advance()

                    while self.tokenizer.getCurrentTokenType() == 'IDENTIFIER':
                        name = self.tokenizer.peekCurrentToken()
                        self.tokenizer.advance()

                        if self.tokenizer.peekCurrentToken() == ',':
                            self.tokenizer.advance()

                        nLocals += 1
                        self.symbol_table.define(name, type, kind)

                    self.tokenizer.advance()    # ;

                self.symbol_table.define_signature(f"{self.symbol_table.class_name}.{subroutine_name}", subroutine_kind, subroutine_type, nArgs, nLocals)

            self.tokenizer.advance()

    def _pretty_xml(self):
        rough_string = ET.tostring(self.root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_xml_string = reparsed.documentElement.toprettyxml(indent="  ")
        # Use this in your re.sub() call
        pretty_xml_string = re.sub(r'\n[ \t]*<!-- -->', '', pretty_xml_string)

        return pretty_xml_string

    def _pretty_vmcode(self):
        return "\n".join(self.vmWriter.vmcode)

    def compile(self):

        if self.tokenizer.peekCurrentToken() == 'class':

            self._buildSymbolTable()
            self.tokenizer.reset()
            self.root = self.compileClass()

        else:
            raise SyntaxError('A Jack file must start with a class declaration.')
        

        if self.mode == 'vm':
            return self._pretty_vmcode()
        else:
            return self._pretty_xml()

    def _process_element(self, parent_element: ET.Element, expected_type=None, expected_value=None):
        
        tags = {
            'STRING_CONST': 'stringConstant',
            'INT_CONST': 'integerConstant',
            'KEYWORD': 'keyword',
            'SYMBOL': 'symbol',
            'IDENTIFIER': 'identifier',
        }

        token_type = self.tokenizer.getCurrentTokenType()
        token_value = self.tokenizer.peekCurrentToken()

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
                
        

        element = ET.SubElement(parent_element, tags[token_type])
        element.text = f' {token_value.strip('\"')} '
        
        self.jackcode_buffer.append(token_value)
        self.tokenizer.advance()

        return element

    def compileClass(self):
        class_element = ET.Element('class')

        # Since the class scope is populated using _buildSymbolTable
        if self.verbose >= 1:
            print(f'\t{'-'*80}')
            print(f'\tClass: {self.symbol_table.class_name}')
            print()
            for var, properties in self.symbol_table.class_scope.items():
                print(f"\t{var:<20}{properties}")
            for var, properties in self.symbol_table.index_counters.items():
                print(f"\t{var:<20}{properties}")
            print()
        
        self._process_element(class_element, 'KEYWORD', 'class')
        self._process_element(class_element, 'IDENTIFIER')
        self._process_element(class_element, 'SYMBOL', '{')

        while self.tokenizer.peekCurrentToken() in ['static', 'field', 'constructor', 'method', 'function']:

            if self.tokenizer.peekCurrentToken() in ['static', 'field']:
                class_element.append(self.compileClassVarDec())

            if self.tokenizer.peekCurrentToken() in ['constructor', 'method', 'function']:
                class_element.append(self.compileSubroutine())

        self._process_element(class_element, 'SYMBOL', '}')

        return class_element

    def compileClassVarDec(self):
        classVarDec_element = ET.Element('classVarDec')

        self._process_element(classVarDec_element, 'KEYWORD', ['static', 'field'])
        self._process_element(classVarDec_element, ['KEYWORD', 'IDENTIFIER'])
        self._process_element(classVarDec_element,'IDENTIFIER')
        while self.tokenizer.peekCurrentToken() == ',':
            self._process_element(classVarDec_element,'SYMBOL', ',')
            self._process_element(classVarDec_element,'IDENTIFIER')

        self._process_element(classVarDec_element,'SYMBOL', ';')

        return classVarDec_element
        
    def compileParameterList(self):
        parameterList_element = ET.Element('parameterList')

        while self.tokenizer.peekCurrentToken() != ')':

            if(self.tokenizer.peekCurrentToken() == ','):
                self._process_element(parameterList_element, 'SYMBOL', ',')
            argType = self.tokenizer.peekCurrentToken()
            self._process_element(parameterList_element, ['KEYWORD', 'IDENTIFIER'])
            argName = self.tokenizer.peekCurrentToken()
            self._process_element(parameterList_element, 'IDENTIFIER')

            self.symbol_table.define(argName, argType, 'arg')
        
        # If the element has no children, give it empty text to prevent self-closing.
        if not list(parameterList_element):
            parameterList_element.append(ET.Comment(" "))


        return parameterList_element

    def compileSubroutine(self):
        # Maybe add the grammar above each for proper documentation!
        '''
        1. Converts the token stream into an xml object and returns
        2. Starts symbol table subroutine after function head
        3. Calls vmwriter after compiling varDecs since local variable count is neccesary for vm function command
        4. If the method happens to be a constructor, pushing the object pointer before return statement is implemented in compileReturn()
        '''

        self.vmWriter.markRecodingStart()

        # subroutine Head
        subroutine_element = ET.Element('subroutineDec')
        subroutine_kind = self.tokenizer.peekCurrentToken()
        self._process_element(subroutine_element, 'KEYWORD', ['constructor', 'function', 'method'])
        self._process_element(subroutine_element, ['KEYWORD', 'IDENTIFIER'])    # type (buildin or user defined)
        name = self.tokenizer.peekCurrentToken()
        self.symbol_table.startSubroutine(name)
        self._process_element(subroutine_element, 'IDENTIFIER')                 #subroutineName
        self._process_element(subroutine_element, 'SYMBOL', '(')
        subroutine_element.append(self.compileParameterList())
        self._process_element(subroutine_element, 'SYMBOL', ')')

        mangled_subroutine_name = f"{self.symbol_table.class_name}.{name}"
        self.vmWriter.writeFunction(mangled_subroutine_name, self.symbol_table.getnLocals(mangled_subroutine_name))
        if subroutine_kind == 'constructor':
            self.vmWriter.writePush('constant', self.symbol_table.index_counters['field'])
            self.vmWriter.writeCall('Memory.alloc', 1)
            self.vmWriter.writePop('pointer', 0)    
        elif subroutine_kind == 'method':
            self.vmWriter.writePush('argument', 0)
            self.vmWriter.writePop('pointer', 0)

        # subroutine Body
        subroutineBody_element = ET.Element('subroutineBody')
        self._process_element(subroutineBody_element, 'SYMBOL', '{')
        while self.tokenizer.peekCurrentToken() == 'var':
            subroutineBody_element.append(self.compileVarDec())
        subroutineBody_element.append(self.compileStatements())
        self._process_element(subroutineBody_element, 'SYMBOL', '}')
        subroutine_element.append(subroutineBody_element)

        self.vmWriter.markRecodingStop()

        if self.verbose >= 2:
            print(f'\t\t{'-'*72}')
            print(f'\t\tSubroutine: {self.symbol_table.subroutine_name}')
            print()
            for var, properties in self.symbol_table.subroutine_scope.items():
                print(f"\t\t{var:<20}{properties}")
            print()
            if self.verbose >= 3:
                print('\t\t--\n')
                print('\t\t', end='')
                print("\n\t\t".join(self.vmWriter.getRecordedBuffer()))
                print()

        return subroutine_element

    def compileVarDec(self):
        varDec_element = ET.Element('varDec')

        varKind = self.tokenizer.peekCurrentToken()
        self._process_element(varDec_element, 'KEYWORD', 'var')
        varType = self.tokenizer.peekCurrentToken()
        self._process_element(varDec_element, ['KEYWORD', 'IDENTIFIER'])
        varName = self.tokenizer.peekCurrentToken()
        self._process_element(varDec_element, 'IDENTIFIER')

        self.symbol_table.define(varName, varType, varKind)

        while self.tokenizer.peekCurrentToken() != ';':
            self._process_element(varDec_element, 'SYMBOL', ',')
            varName = self.tokenizer.peekCurrentToken()
            self._process_element(varDec_element, 'IDENTIFIER')

            self.symbol_table.define(varName, varType, varKind)

        self._process_element(varDec_element, 'SYMBOL', ';')

        return varDec_element

    def compileStatements(self):
        statements_element = ET.Element('statements')

        while self.tokenizer.peekCurrentToken() in ['let', 'if', 'while', 'do', 'return']:

            if self.tokenizer.peekCurrentToken() == 'let':
                statements_element.append(self.compileLet())

            elif self.tokenizer.peekCurrentToken() == 'if':
                statements_element.append(self.compileIf())

            elif self.tokenizer.peekCurrentToken() == 'while':
                statements_element.append(self.compileWhile())

            elif self.tokenizer.peekCurrentToken() == 'do':
                statements_element.append(self.compileDo())

            elif self.tokenizer.peekCurrentToken() == 'return':
                statements_element.append(self.compileReturn())

                # If the element has no children, give it empty text to prevent self-closing.
        if not list(statements_element):
            statements_element.append(ET.Comment(" "))


        return statements_element

    def compileLet(self):
        let_element = ET.Element('letStatement')

        self._process_element(let_element, 'KEYWORD', 'let')
        lvalueName = self.tokenizer.peekCurrentToken()
        self._process_element(let_element, 'IDENTIFIER')

        lvalue_indexing = self.symbol_table.typeOf(lvalueName) == 'Array' and self.tokenizer.peekCurrentToken() == '['
    
        if lvalue_indexing:

            seg, idx = self._getSegmentAndIndex(lvalueName)
            self.vmWriter.writePush(seg, idx)

            self._process_element(let_element, 'SYMBOL', '[')
            let_element.append(self.compileExpression())
            self._process_element(let_element, 'SYMBOL', ']')

            self.vmWriter.writeArthmetic('+')
            self.vmWriter.writePop('temp', 0)

        self._process_element(let_element, 'SYMBOL', '=')
        let_element.append(self.compileExpression())
        self._process_element(let_element, 'SYMBOL', ';')

        if lvalue_indexing:
            self.vmWriter.writePush('temp', 0)
            self.vmWriter.writePop('pointer', 0)
            self.vmWriter.writePop('this', 0)

        else:
            seg, idx = self._getSegmentAndIndex(lvalueName)
            self.vmWriter.writePop(seg, idx)

        return let_element

    def compileIf(self):
        if_element = ET.Element('ifStatement')
        
        label_true, label_false, label_end = self.symbol_table._getBaseLabel(['true', 'false', 'end'])

        self._process_element(if_element, 'KEYWORD', 'if')
        self._process_element(if_element, 'SYMBOL', '(')
        if_element.append(self.compileExpression())
        self._process_element(if_element, 'SYMBOL', ')')

        self.vmWriter.writeIf(label_true)
        self.vmWriter.writeGoto(label_false)

        self.vmWriter.writeLabel(label_true)
        self._process_element(if_element, 'SYMBOL', '{')
        if_element.append(self.compileStatements())
        self._process_element(if_element, 'SYMBOL', '}')

        # Jumping past the label_false
        self.vmWriter.writeGoto(label_end)

        self.vmWriter.writeLabel(label_false)  

        if self.tokenizer.peekCurrentToken() == 'else':
            self._process_element(if_element, 'KEYWORD', 'else')
            self._process_element(if_element, 'SYMBOL', '{')
            if_element.append(self.compileStatements())
            self._process_element(if_element, 'SYMBOL', '}')

        self.vmWriter.writeLabel(label_end)

        return if_element

    def compileWhile(self):
        while_element = ET.Element('whileStatement')

        label_condition, label_begin, label_end = self.symbol_table._getBaseLabel(['condition', 'begin', 'end'])
        
        self.vmWriter.writeLabel(label_condition)

        self._process_element(while_element, 'KEYWORD', 'while')
        self._process_element(while_element, 'SYMBOL', '(')
        while_element.append(self.compileExpression())
        self._process_element(while_element, 'SYMBOL', ')')

        self.vmWriter.writeIf(label_begin)
        self.vmWriter.writeGoto(label_end)

        self.vmWriter.writeLabel(label_begin)
        self._process_element(while_element, 'SYMBOL', '{')
        while_element.append(self.compileStatements())
        self._process_element(while_element, 'SYMBOL', '}')

        self.vmWriter.writeGoto(label_condition)
        self.vmWriter.writeLabel(label_end)

        return while_element

    def compileDo(self):
        do_element = ET.Element('doStatement')
        self._process_element(do_element, 'KEYWORD', 'do')
        self._compileSubroutineCall(do_element)
        self._process_element(do_element, 'SYMBOL', ';')
        self.vmWriter.writePop('temp', 0)
        return do_element
   
    def _compileSubroutineCall(self, parent_element):
        subroutineName = ''

        className = self.tokenizer.peekCurrentToken()
        self._process_element(parent_element, 'IDENTIFIER')
        if self.tokenizer.peekCurrentToken() == '.':
            # Implies that this subroutine is an object method
            self._process_element(parent_element, 'SYMBOL', '.')
            subroutineName = self.tokenizer.peekCurrentToken()
            self._process_element(parent_element, 'IDENTIFIER')
        else:
            # The function must be defined in the class scope, reassign className to subroutine name
            subroutineName = className
            className = self.symbol_table.class_name
    
        self._process_element(parent_element, 'SYMBOL', '(')
        expressionList = self.compileExpressionList()
        parent_element.append(expressionList)
        self._process_element(parent_element, 'SYMBOL', ')')

        subroutineCall_args = [child for child in list(expressionList) if child.tag == 'expression']
        nArgs = len(subroutineCall_args)

        # Consulting the symbol table for the class name in case 'className' is an object
        if className in self.symbol_table:
            # A method call on an object called className
            className = self.symbol_table.typeOf(className)
            
        if className == self.symbol_table.class_name:
            # Addressing the first object push
            self.vmWriter.writePush('pointer', 0)
            nArgs += 1

        subroutineName = f'{className}.{subroutineName}'
        self.vmWriter.writeCall(subroutineName, nArgs)

    def compileReturn(self):
        return_element = ET.Element('returnStatement')

        self._process_element(return_element, 'KEYWORD', 'return')
        if self.tokenizer.peekCurrentToken() != ';':
            return_element.append(self.compileExpression())
        self._process_element(return_element, 'SYMBOL', ';')        # ';'

        if self.symbol_table.subroutine_type == 'void':
            self.vmWriter.writePush('constant', 0)
        self.vmWriter.writeReturn()

        return return_element

    def compileExpressionList(self):
        expressionList_element = ET.Element('expressionList')
        while self.tokenizer.peekCurrentToken() != ')':
            if self.tokenizer.peekCurrentToken() == ',':
                self._process_element(expressionList_element, 'SYMBOL', ',')
            expressionList_element.append(self.compileExpression())

        # If the element has no children, give it empty text to prevent self-closing.
        if not list(expressionList_element):
            expressionList_element.append(ET.Comment(" "))

        return expressionList_element

    def compileExpression(self):
        expression_element = ET.Element('expression')

        expression_element.append(self.compileTerm())
        while self.tokenizer.peekCurrentToken() in '+-*/&|<>=':
            operation = self.tokenizer.peekCurrentToken()
            self._process_element(expression_element, 'SYMBOL')
            expression_element.append(self.compileTerm())

            self.vmWriter.writeArthmetic(operation)
        
        return expression_element
    
    def _getSegmentAndIndex(self, varName):

        segment_map = {
            'arg': 'argument',
            'var': 'local',
            'field': 'this',
            'static': 'static'
        }

        segment = segment_map[self.symbol_table.kindOf(varName)]
        index = self.symbol_table.indexOf(varName)

        return (segment, index)
        
    def compileTerm(self):
        term_element = ET.Element('term')

        token_type = self.tokenizer.getCurrentTokenType()
        token_value = self.tokenizer.peekCurrentToken()

        if token_type in ['INT_CONST', 'STRING_CONST']:
            if token_type == 'INT_CONST':
                self.vmWriter.writePush('constant', self.tokenizer.peekCurrentToken())
            elif token_type == 'STRING_CONST':

                string = token_value.strip('\"')

                # Creating the string object
                self.vmWriter.writePush('constant', len(string))
                self.vmWriter.writeCall('String.new', 1)

                # Adding each character to the string object created
                for c in string:
                    self.vmWriter.writePush('constant', ord(c))
                    self.vmWriter.writeCall('String.appendChar', 2)
                

            self._process_element(term_element, token_type)
        elif token_value in ['true', 'false', 'null', 'this']:
            if token_value == 'true':
                self.vmWriter.writePush('constant', '0')
                self.vmWriter.writePush('constant', '1')
                self.vmWriter.writeArthmetic('-')
            elif token_value == 'false':
                self.vmWriter.writePush('constant', '0')
            elif token_value == 'this':
                self.vmWriter.writePush('pointer', '0')
            else:
                raise ValueError('Not setup yet!')
            self._process_element(term_element, 'KEYWORD')
        elif token_value in ['~', '-']:
            unary_op = self.tokenizer.peekCurrentToken()
            self._process_element(term_element, 'SYMBOL', ['~', '-'])
            term_element.append(self.compileTerm())
            if unary_op == '-':
                self.vmWriter.writeArthmetic('NEG')
            else:
                self.vmWriter.writeArthmetic('NOT')
        elif token_value == '(':
            self._process_element(term_element, 'SYMBOL', '(')
            term_element.append(self.compileExpression())
            self._process_element(term_element, 'SYMBOL', ')')
        elif token_type == 'IDENTIFIER':
            next_token = self.tokenizer.peekNextToken()
            if next_token in ('.', '('):
                self._compileSubroutineCall(term_element)
            else:
                varName = self.tokenizer.peekCurrentToken()
                self._process_element(term_element, 'IDENTIFIER') # varName

                segment, index = self._getSegmentAndIndex(varName)
                self.vmWriter.writePush(segment, index)

                if self.tokenizer.peekCurrentToken() == '[':
                    # Array
                    self._process_element(term_element, 'SYMBOL', '[')
                    term_element.append(self.compileExpression())
                    self._process_element(term_element, 'SYMBOL', ']')

                    self.vmWriter.writeArthmetic('+')
                    self.vmWriter.writePop('pointer', 1)
                    self.vmWriter.writePush('that', 0)

        else:
            raise SyntaxError(f"Unexpected token in term: {token_value}")

        return term_element



import argparse

if __name__ == '__main__':

    # Flag configurations
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, choices=['vm', 'xml'], default='vm')
    parser.add_argument('--input', type=str, default='D:\\NANDtoTETRIS\\projects\\11\\Seven')


    args = parser.parse_args()

    # Define the input and output file paths
    # IMPORTANT: Update this path to where your Jack file is located.
    input_jack_file = args.input
    output_xml_file = 'Main.xml' # This will be created in the same directory as the script
    output_vmcode_file = 'Main.vm'

    try:
        # Read the source Jack code from the input file
        with open(input_jack_file, 'r') as f:
            jack_code = f.read()

        # Initialize the tokenizer and compilation engine
        tokenizer = JackTokenizer(jack_code)
        vm_writer = VMWriter()
        compilation_engine = CompilationEngine(tokenizer, vm_writer)

        compilation_engine.compile()
        print("\n".join(vm_writer.vmcode))



    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_jack_file}'")
    except SyntaxError as e:
        print(f"A syntax error occurred during compilation: {e}")
