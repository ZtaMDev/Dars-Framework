from typing import Optional
from .script import Script

class dScript(Script):
    """
    Script that can be defined as inline (JS code in string) or as a reference to an external file.
    Only one of the two must be present.
    """
    def __init__(self, code: Optional[str] = None, file_path: Optional[str] = None, target_language: str = "javascript"):
        super().__init__(target_language)
        if (code is None and file_path is None) or (code is not None and file_path is not None):
            raise ValueError("You have to specify only one: 'code' (inline) or 'file_path' (external), but not both.")
        self.code = code
        self.file_path = file_path

    def get_code(self) -> str:
        if self.code is not None:
            return self.code
        elif self.file_path is not None:
            try:
                with open(self.file_path, 'r') as f:
                    return f.read()
            except FileNotFoundError:
                raise FileNotFoundError(f"The script file was not found: {self.file_path}")
        else:
            raise ValueError("No code or file path defined for this dScript.")
