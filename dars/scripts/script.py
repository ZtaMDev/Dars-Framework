from abc import ABC, abstractmethod
from typing import Optional

class Script(ABC):
    """Base class for script definitions"""
    def __init__(self, target_language: str = "javascript"):
        if target_language not in ["javascript", "typescript"]:
            raise ValueError("The target language must be 'javascript' or 'typescript'")
        self.target_language = target_language
        
    @abstractmethod
    def get_code(self) -> str:
        """Returns the script code in the target language"""
        pass

class InlineScript(Script):
    """Script defined directly in Python code"""
    def __init__(self, code: str, target_language: str = "javascript"):
        super().__init__(target_language)
        self.code = code
        
    def get_code(self) -> str:
        return self.code
        
class FileScript(Script):
    """Script loaded from an external file"""
    def __init__(self, file_path: str, target_language: str = "javascript"):
        super().__init__(target_language)
        self.file_path = file_path
        
    def get_code(self) -> str:
        try:
            with open(self.file_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"The script file was not found: {self.file_path}")


