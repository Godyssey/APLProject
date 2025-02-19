from lexer_module.lexer import tokenize
from parser_module.parser_mod import parse

def compile_apbl(file_path):
    """Compile an APBL source file"""
    try:
        # Read source code
        with open(file_path, 'r') as f:
            source_code = f.read()
        
        # Step 1: Lexical Analysis
        tokens = tokenize(source_code)
        if not tokens:
            print("Lexical analysis failed")
            return False
        
        # Step 2: Syntax Analysis
        ast = parse(tokens)
        if not ast:
            print("Syntax analysis failed")
            return False
        
        return True
            
    except Exception as e:
        print(f"Error compiling APBL file: {str(e)}")
        return False

# Entry point
if __name__ == "__main__":
    compile_apbl("sample_code.apbl")