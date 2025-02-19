def write_lexical_analysis(tokens):
    """Write lexical analysis results to file"""
    with open('lexer_module/lexical_analysis.txt', 'w', encoding='utf-8') as f:
        f.write("LEXICAL ANALYSIS\n")
        f.write("================\n\n")
        for tok in tokens:
            f.write(f"Line {tok.lineno}: {tok.type}({tok.value})\n")

def write_syntax_analysis(ast):
    """Write syntax analysis (AST) to file"""
    with open('parser_module/syntax_analysis.txt', 'w', encoding='utf-8') as f:
        f.write("SYNTAX ANALYSIS\n")
        f.write("===============\n\n")
        if ast:
            write_ast(ast, f)
        else:
            f.write("Failed to generate AST\n")

def write_ast(node, file, level=0):
    """Write AST node to file"""
    indent = "  " * level
    
    if isinstance(node, dict):
        # Write node type
        file.write(f"{indent}{node['type']}")
        
        # Add name if present
        if 'name' in node:
            file.write(f" '{node['name']}'")
            
        # Add type info
        if 'data_type' in node:
            if isinstance(node['data_type'], dict):
                file.write(f" : {node['data_type']['name']}")
            else:
                file.write(f" : {node['data_type']}")
                
        # Add value for literals
        if 'value' in node and not isinstance(node['value'], (dict, list)):
            file.write(f" = {node['value']}")
            
        # Add operator for binary operations
        if 'op' in node:
            file.write(f" [{node['op']}]")
            
        file.write("\n")
        
        # Process children in specific order
        for key in ['statements', 'condition', 'then_block', 'else_block', 
                   'body', 'left', 'right', 'params']:
            if key in node and node[key]:
                if key in ['then_block', 'else_block']:
                    file.write(f"{indent}  {key.split('_')[0]}:\n")
                    write_ast(node[key], file, level + 2)
                else:
                    write_ast(node[key], file, level + 1)
    
    elif isinstance(node, list):
        for item in node:
            write_ast(item, file, level) 