# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
from abc import ABC, abstractmethod
from typing import Optional

class Script(ABC):
    """Base class for script definitions"""
    def __init__(self, target_language: str = "javascript", module: bool = False):
        if target_language not in ["javascript", "typescript"]:
            raise ValueError("The target language must be 'javascript' or 'typescript'")
        self.target_language = target_language
        self.module = module
        
    @abstractmethod
    def get_code(self) -> str:
        """Returns the script code in the target language"""
        pass

class InlineScript(Script):
    """Script defined directly in Python code"""
    def __init__(self, code: str, target_language: str = "javascript", module: bool = False):
        super().__init__(target_language, module=module)
        self.code = code
        
    def get_code(self) -> str:
        return self.code
        
class FileScript(Script):
    """Script loaded from an external file"""
    def __init__(self, file_path: str, target_language: str = "javascript", module: bool = False):
        super().__init__(target_language, module=module)
        self.file_path = file_path
        
    def get_code(self) -> str:
        try:
            with open(self.file_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"The script file was not found: {self.file_path}")


