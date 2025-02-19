class CompilationError:
    def __init__(self, phase, message, line, column=None, value=None):
        self.phase = phase
        self.message = message
        self.line = line
        self.column = column
        self.value = value
    
    def __str__(self):
        msg = f"{self.message} at line {self.line}"
        if self.column:
            msg += f", column {self.column}"
        if self.value:
            msg += f": '{self.value}'"
        return msg

class ErrorCollector:
    def __init__(self):
        self.errors = []
    
    def add_error(self, phase, message, line, column=None, value=None):
        error = CompilationError(phase, message, line, column, value)
        self.errors.append(error)
    
    def has_errors(self):
        return len(self.errors) > 0
    
    def report_errors(self):
        if not self.errors:
            return False
            
        # Sort ALL errors by line number
        self.errors.sort(key=lambda e: (e.line, e.phase != 'syntax'))
        
        # Group by phase while maintaining order
        syntax_errors = [e for e in self.errors if e.phase == 'syntax']
        semantic_errors = [e for e in self.errors if e.phase == 'semantic']
        
        # Print all errors in order
        if syntax_errors:
            print("\nSyntax Errors:")
            for i, error in enumerate(syntax_errors, 1):
                print(f"{i}. {error}")
                
        if semantic_errors:
            print("\nSemantic Errors:")
            for i, error in enumerate(semantic_errors, 1):
                print(f"{i}. {error}")
                
        print(f"\nTotal Errors: {len(self.errors)}")
        return True 