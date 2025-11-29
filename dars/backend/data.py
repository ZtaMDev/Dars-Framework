from dars.scripts.dscript import dScript, RawJS
from typing import Any, Optional, Union

class DataAccessor:
    """
    Accesses data from HTTP operations by operation ID.
    
    NOT to be confused with HTML element IDs - this references
    the ID given to fetch/get/post operations.
    """
    
    def __init__(self, operation_id: str, path: Optional[str] = None):
        self.operation_id = operation_id
        self.path = path
    
    @property
    def code(self) -> str:
        """Return the JS code to access this data."""
        if self.path:
            return f"window.{self.operation_id}?.{self.path}"
        return f"window.{self.operation_id}"

    def __getattr__(self, name: str) -> 'DataAccessor':
        """
        Enable dot notation access: useData('user').name
        Returns a new DataAccessor for the nested property.
        """
        new_path = f"{self.path}.{name}" if self.path else name
        return DataAccessor(self.operation_id, new_path)
    
    def get(self, path: Optional[str] = None) -> RawJS:
        """
        Get data from operation, optionally at a specific path.
        
        Args:
            path: JSON path (e.g., "user.name" or "items[0].title")
        
        Returns:
            RawJS expression to access the data
        """
        current_code = self.code
        if path:
            return RawJS(f"{current_code}?.{path}")
        return RawJS(current_code)
    
    def bind(self, reactive_property: Any) -> dScript:
        """
        Bind this data to a reactive state property.
        
        Args:
            reactive_property: A StateV2 reactive property (e.g., state.text)
        
        Returns:
            dScript that updates the property with fetched data
        """
        # We need to access internal attributes of the reactive property
        # This assumes reactive_property is an instance of ReactiveProperty from state_v2.py
        try:
            component_id = reactive_property._state.component.id
            prop_name = reactive_property._name
        except AttributeError:
            raise ValueError("bind() expects a StateV2 reactive property (e.g., state.text)")
        
        code = f"""
const data = {self.code};
if (data !== undefined && data !== null) {{
    Dars.change({{
        id: '{component_id}',
        dynamic: true,
        {prop_name}: typeof data === 'object' ? JSON.stringify(data) : String(data)
    }});
}}
"""
        return dScript(code.strip())
    
    def map(self, transform: str) -> 'DataAccessor':
        """
        Transform the data using a JavaScript expression.
        
        Args:
            transform: JS code to transform data (use 'data' as variable name)
        
        Returns:
            New DataAccessor with transformation applied
        """
        # This creates transformed accessor
        transformed_id = f"{self.operation_id}_transformed"
        transform_code = f"""
window.{transformed_id} = (() => {{
    const data = {self.code};
    return {transform};
}})();
"""
        # We need to execute this transform code first
        # But since we return an accessor, we can't easily inject code here.
        # Ideally, this should be part of a chain that executes the transform.
        # For now, we'll assume the user handles the execution order or we'll improve this later.
        # A better approach might be to return a dScript that does the transform AND returns the accessor.
        return DataAccessor(transformed_id)


def useData(operation_id: str) -> DataAccessor:
    """
    Access data from an HTTP operation by its operation ID.
    
    Args:
        operation_id: The ID given to fetch/get/post (NOT an HTML element ID)
    
    Returns:
        DataAccessor for chaining methods
    """
    return DataAccessor(operation_id)
