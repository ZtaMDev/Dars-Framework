from abc import ABC, abstractmethod
from typing import Optional

class Script(ABC):
    """Clase base para la definición de scripts"""
    def __init__(self, target_language: str = "javascript"):
        if target_language not in ["javascript", "typescript"]:
            raise ValueError("El lenguaje objetivo debe ser 'javascript' o 'typescript'")
        self.target_language = target_language
        
    @abstractmethod
    def get_code(self) -> str:
        """Retorna el código del script en el lenguaje objetivo"""
        pass

class InlineScript(Script):
    """Script definido directamente en el código Python"""
    def __init__(self, code: str, target_language: str = "javascript"):
        super().__init__(target_language)
        self.code = code
        
    def get_code(self) -> str:
        return self.code
        
class FileScript(Script):
    """Script cargado desde un archivo externo"""
    def __init__(self, file_path: str, target_language: str = "javascript"):
        super().__init__(target_language)
        self.file_path = file_path
        
    def get_code(self) -> str:
        try:
            with open(self.file_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"El archivo de script no se encontró: {self.file_path}")


