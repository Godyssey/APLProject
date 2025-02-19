def print_tree(node, level=0, is_last=True, file=None):
    """Utility function to visualize the Abstract Syntax Tree (AST)
    
    Args:
        node: Current node in the AST
        level: Current indentation level (default: 0)
        is_last: Whether this is the last child in its parent (default: True)
        file: Optional file object for writing output (default: None, prints to console)
    """
    # Base case: return if node is None
    if not node:
        return
        
    try:
        # Create the appropriate indentation with tree-like structure
        # Uses │ for vertical lines and ├── or └── for branches
        indent = "│   " * (level - 1) + ("└── " if is_last else "├── ") if level > 0 else ""
        
        # Handle dictionary nodes (AST nodes with attributes)
        if isinstance(node, dict):

            # Build node description with type, name, data_type, and operator if present
            desc = node.get('type', 'unknown')  # Safely get node type with default
            if 'name' in node:
                desc += f" '{node['name']}'"

            if 'data_type' in node and node['data_type']:
                # Handle both string and dictionary data types
                if isinstance(node['data_type'], dict) and 'name' in node['data_type']:
                    desc += f" : {node['data_type']['name']}"
                else:
                    desc += f" : {node['data_type']}"

            if 'op' in node:
                desc += f" [{node['op']}]"
            
            # Print the node description
            print(f"{indent}{desc}", file=file)
            
            # Prepare to handle node's children and attributes
            items = []
            
            # Keys to skip in the output for cleaner visualization
            skip_keys = {'type', 'name', 'data_type', 'op', 'line', 'column', 'scope', 'symbol_table'}
            
            # Special handling for value attributes
            if 'value' in node:
                if isinstance(node['value'], (dict, list)):
                    items.append(('value', node['value']))
                else:
                    # For simple values, print and return
                    print(f"{indent}└── value = {node['value']}", file=file)
                    return
            
            # Collect all other relevant attributes
            for key, value in node.items():
                if key not in skip_keys and key != 'value' and value is not None:
                    items.append((key, value))
            
            # Define order of attributes for consistent output
            priority_keys = ['condition', 'left', 'right', 'then_block', 'else_block', 
                           'return_type', 'params', 'body', 'statements']
            
            # Sort items based on priority and then alphabetically
            items.sort(key=lambda x: (
                priority_keys.index(x[0]) if x[0] in priority_keys else len(priority_keys),
                x[0]
            ))
            
            # Print each child/attribute
            for i, (key, value) in enumerate(items):
                is_last_child = i == len(items) - 1
                child_indent = indent + ("└── " if is_last_child else "├── ")
                
                if isinstance(value, (dict, list)):
                    # Recursively print nested structures
                    print(f"{child_indent}{key}:", file=file)
                    next_level = level + (2 if level > 0 else 1)
                    print_tree(value, next_level, True, file)
                else:
                    # Print simple values directly
                    print(f"{child_indent}{key}: {value}", file=file)
                
        # Handle list nodes (collections of AST nodes)
        elif isinstance(node, list):
            for i, item in enumerate(node):
                print_tree(item, level, i == len(node) - 1, file)
        # Handle simple values
        else:
            print(f"{indent}{node}", file=file)
            
    except UnicodeEncodeError:
        # Error Handling: Fall back to ASCII characters if Unicode fails
        # This can happen when writing to files with certain encodings
        indent = "|   " * (level - 1) + ("+-- " if is_last else "+-- ") if level > 0 else ""
        print(f"{indent}{str(node)}", file=file)
    except Exception as e:
        # Error Handling: Log any other errors but continue processing
        # This ensures one bad node doesn't stop the entire tree from being printed
        print(f"Warning: Error processing node: {str(e)}", file=file) 