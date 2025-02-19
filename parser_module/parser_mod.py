import ply.yacc as yacc
from lexer_module.lexer import tokens
from utils.output_handler import write_syntax_analysis

# -----------------------------------------------------------------------------
# Precedence Rules
# -----------------------------------------------------------------------------
precedence = (
    ('nonassoc', 'LE', 'GE', 'LT', 'GT', 'EQ', 'NEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# -----------------------------------------------------------------------------
# Helper: AST Node Creation
# -----------------------------------------------------------------------------
def create_node(type, **kwargs):
    """Create an AST node with common attributes."""
    return {
        'type': type,
        'line': kwargs.get('line', 0),
        'column': kwargs.get('column', 0),
        **kwargs
    }

# -----------------------------------------------------------------------------
# Program and Statement List
# -----------------------------------------------------------------------------
def p_program(p):
    '''program : statement_list'''
    p[0] = create_node('program', statements=p[1] if p[1] else [])

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement_list_opt(p):
    '''statement_list_opt : statement_list
                          | empty'''
    p[0] = p[1] if p[1] is not None else []

# -----------------------------------------------------------------------------
# Statements
# -----------------------------------------------------------------------------
def p_statement(p):
    '''statement : declaration_stmt
                 | assignment_stmt
                 | function_def_stmt
                 | function_call_stmt
                 | if_stmt
                 | while_stmt
                 | return_stmt'''
    p[0] = p[1]

# -----------------------------------------------------------------------------
# Declarations and Type Specifiers
# -----------------------------------------------------------------------------
def p_declaration_stmt(p):
    '''declaration_stmt : type_specifier IDENTIFIER EQUALS expression EOL'''
    p[0] = create_node('declaration',
                       var_type=p[1],
                       name=p[2],
                       value=p[4],
                       line=p.lineno(1))

def p_type_specifier(p):
    '''type_specifier : INT_TYPE
                      | FLOAT_TYPE
                      | STRING_TYPE
                      | BOOL_TYPE
                      | DATE_TYPE
                      | TIME_TYPE
                      | VOID'''
    p[0] = p[1]

# -----------------------------------------------------------------------------
# Assignment
# -----------------------------------------------------------------------------
def p_assignment_stmt(p):
    '''assignment_stmt : IDENTIFIER EQUALS expression EOL'''
    p[0] = create_node('assignment',
                       target=p[1],
                       value=p[3],
                       line=p.lineno(1))

# -----------------------------------------------------------------------------
# Function Definitions and Parameters
# -----------------------------------------------------------------------------
def p_function_def_stmt(p):
    '''function_def_stmt : FUNCTION type_specifier IDENTIFIER LPAREN param_list RPAREN block_stmt'''
    p[0] = create_node('function_def',
                       return_type=p[2],
                       name=p[3],
                       params=p[5],
                       body=p[7],
                       line=p.lineno(1))

def p_param_list(p):
    '''param_list : param_list COMMA param
                  | param
                  | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif p[1] is None:
        p[0] = []
    else:
        p[0] = [p[1]]

def p_param(p):
    '''param : type_specifier IDENTIFIER'''
    p[0] = create_node('parameter',
                       param_type=p[1],
                       name=p[2],
                       line=p.lineno(1))

# -----------------------------------------------------------------------------
# Block Statements
# -----------------------------------------------------------------------------
def p_block_stmt(p):
    '''block_stmt : LBRACKET statement_list_opt RBRACKET'''
    p[0] = create_node('block', statements=p[2])

# -----------------------------------------------------------------------------
# Function Calls
# -----------------------------------------------------------------------------
def p_callable(p):
    '''callable : IDENTIFIER
                | BOOK
                | GEN
                | REG
                | DISPLAY'''
    p[0] = p[1]

def p_function_call_stmt(p):
    '''function_call_stmt : function_call EOL'''
    p[0] = p[1]

def p_function_call(p):
    '''function_call : callable LPAREN arg_list RPAREN'''
    p[0] = create_node('function_call',
                       name=p[1],
                       arguments=p[3],
                       line=p.lineno(1))

def p_arg_list(p):
    '''arg_list : arg_list COMMA expression
                | expression
                | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif p[1] is None:
        p[0] = []
    else:
        p[0] = [p[1]]

# -----------------------------------------------------------------------------
# Control Structures
# -----------------------------------------------------------------------------
def p_if_stmt(p):
    '''if_stmt : IF LPAREN expression RPAREN block_stmt
               | IF LPAREN expression RPAREN block_stmt ELSE block_stmt'''
    if len(p) == 6:
        p[0] = create_node('if',
                           condition=p[3],
                           then_block=p[5],
                           line=p.lineno(1))
    else:
        p[0] = create_node('if',
                           condition=p[3],
                           then_block=p[5],
                           else_block=p[7],
                           line=p.lineno(1))

def p_while_stmt(p):
    '''while_stmt : WHILE LPAREN expression RPAREN block_stmt'''
    p[0] = create_node('while',
                       condition=p[3],
                       body=p[5],
                       line=p.lineno(1))

def p_return_stmt(p):
    '''return_stmt : RETURN expression EOL'''
    p[0] = create_node('return',
                       value=p[2],
                       line=p.lineno(1))

# -----------------------------------------------------------------------------
# Unified Expression Productions
# -----------------------------------------------------------------------------
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression LE expression
                  | expression GE expression
                  | expression LT expression
                  | expression GT expression
                  | expression EQ expression
                  | expression NEQ expression'''
    p[0] = create_node('binary_op',
                       op=p[2],
                       left=p[1],
                       right=p[3],
                       line=p.lineno(2))

def p_expression_paren(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_atom(p):
    '''expression : NUMBER
                  | FLOAT_NUM
                  | STRING_LITERAL
                  | BOOLEAN_VAL
                  | DATE_VAL
                  | TIME_VAL
                  | IDENTIFIER
                  | function_call'''
    token_type = p.slice[1].type
    if token_type in ('NUMBER', 'FLOAT_NUM', 'STRING_LITERAL', 'BOOLEAN_VAL', 'DATE_VAL', 'TIME_VAL'):
        p[0] = create_node('literal', value=p[1], line=p.lineno(1))
    elif token_type == 'IDENTIFIER':
        p[0] = create_node('identifier', name=p[1], line=p.lineno(1))
    else:
        p[0] = p[1]

# -----------------------------------------------------------------------------
# Empty Production
# -----------------------------------------------------------------------------
def p_empty(p):
    'empty :'
    p[0] = None

# -----------------------------------------------------------------------------
# Error Handling
# -----------------------------------------------------------------------------
def p_error(p):
    if p:
        print(f"Syntax error at line {p.lineno}, token={p.type}, value={p.value}")
    else:
        print("Syntax error at EOF")

# -----------------------------------------------------------------------------
# Build the Parser
# -----------------------------------------------------------------------------
parser = yacc.yacc(debug=True, optimize=False, errorlog=yacc.NullLogger())

# -----------------------------------------------------------------------------
# Token Stream Wrapper
# -----------------------------------------------------------------------------
class TokenStream:
    """
    A simple wrapper that accepts a list of tokens and provides
    the token() method required by PLY.
    """
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
    def token(self):
        if self.index < len(self.tokens):
            tok = self.tokens[self.index]
            self.index += 1
            return tok
        return None
    @property
    def lineno(self):
        if self.index < len(self.tokens):
            return getattr(self.tokens[self.index], 'lineno', 0)
        return 0

# -----------------------------------------------------------------------------
# Parse Function
# -----------------------------------------------------------------------------
def parse(token_list):
    """
    Accepts a list of tokens (produced by the lexer) and returns the AST.
    """
    try:
        ts = TokenStream(token_list)
        ast = parser.parse(lexer=ts, tracking=True)
        write_syntax_analysis(ast)
        return ast
    except Exception as e:
        print(f"Parsing error: {str(e)}")
        return None
