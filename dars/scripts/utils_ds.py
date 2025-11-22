"""Utility functions for creating common dScript patterns"""
from dars.scripts.dscript import dScript


def showModal(id: str) -> dScript:
    """
    Returns a dScript that shows a Dars Modal component.
    
    Args:
        id: The ID of the modal component to show
        
    Returns:
        dScript object that removes hidden attributes and displays the modal
        
    Example:
        Button("Open Modal", on_click=showModal(id="my-modal"))
    """
    code = f"const m = document.getElementById('{id}'); m.removeAttribute('hidden'); m.classList.remove('dars-modal-hidden'); m.style.display = 'flex';"
    return dScript(code)


def hideModal(id: str) -> dScript:
    """
    Returns a dScript that hides a Dars Modal component.
    
    Args:
        id: The ID of the modal component to hide
        
    Returns:
        dScript object that adds hidden attributes and hides the modal
        
    Example:
        Button("Close Modal", on_click=hideModal(id="my-modal"))
    """
    code = f"const m = document.getElementById('{id}'); m.setAttribute('hidden', ''); m.classList.add('dars-modal-hidden'); m.style.display = 'none';"
    return dScript(code)
