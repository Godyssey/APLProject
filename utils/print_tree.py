def print_tree(node, level=0, is_last=True):
    """Visualize the Abstract Syntax Tree in a hierarchical format
    
    Args:
        node: Current AST node being processed
        level: Current indentation level (default: 0)
        is_last: Whether this is the last child in its parent list (default: True)
    """
    if not node:
        return
    
    # Create appropriate indentation with tree branches
    indent = "  " * (level - 1) + ("└── " if is_last else "├── ") if level > 0 else ""
    
    if isinstance(node, dict):
        # Build node description with all relevant information
        desc = node['type']
        if 'name' in node:
            desc += f" '{node['name']}'"
        if 'value' in node and isinstance(node['value'], (int, float, str, bool)):
            desc += f" = {node['value']}"
        if 'data_type' in node and node['data_type']:
            desc += f" : {node['data_type']}"
        if 'op' in node:
            desc += f" [{node['op']}]"
        print(f"{indent}{desc}")
        
        # Process attributes in a specific order for consistent output
        items = []
        if node['type'] == 'program' and 'statements' in node:
            items.append(('statements', node['statements']))
        if 'left' in node: items.append(('left', node['left']))
        if 'right' in node: items.append(('right', node['right']))
        if 'condition' in node: items.append(('condition', node['condition']))
        if 'then_block' in node: items.append(('then', node['then_block']))
        if 'else_block' in node: items.append(('else', node['else_block']))
        if 'body' in node: items.append(('body', node['body']))
        if 'params' in node: items.append(('params', node['params']))
        if 'statements' in node and node['type'] != 'program': 
            items.append(('statements', node['statements']))
        
        # Print each child/attribute with appropriate tree branches
        for i, (key, value) in enumerate(items):
            is_last_child = i == len(items) - 1
            if value:  # Skip empty children
                print(f"{indent}{'└── ' if is_last_child else '├── '}{key}:")
                print_tree(value, level + 2, is_last_child)
    
    # Handle lists of nodes (e.g., statement lists)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            print_tree(item, level + 1, i == len(node) - 1)
    
    # Handle simple values (e.g., identifiers, literals)
    else:
        print(f"{indent}{node}") 