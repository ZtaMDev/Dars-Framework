import importlib, inspect, sys, os
from dars.core.component import Component
from dars.components.basic.text import Text

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dars'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

failures = []

def test_advanced_components():
    base_pkg = 'dars.components.advanced'
    try:
        pkg = importlib.import_module(base_pkg)
    except Exception as e:
        raise AssertionError(f'Could not import {base_pkg}: {e}')
    
    pkg_path = os.path.dirname(pkg.__file__)
    for fname in os.listdir(pkg_path):
        if not fname.endswith('.py') or fname.startswith('__'):
            continue
        
        modname = f"{base_pkg}.{fname[:-3]}"
        try:
            m = importlib.import_module(modname)
        except Exception as e:
            failures.append((modname, 'import', repr(e)))
            continue
        
        for _name, obj in inspect.getmembers(m, inspect.isclass):
            try:
                if obj is Component: 
                    continue
                if issubclass(obj, Component):
                    # Proporciona argumentos específicos para cada componente avanzado
                    if _name == 'Accordion':
                        instance = obj(sections=[{'title': 'Test', 'content': 'Content'}])
                    elif _name == 'Table':
                        instance = obj(columns=['Col1'], data=[['Data1']])
                    elif _name == 'Tabs':
                        instance = obj(tabs=['Tab1'], panels=[Text('Panel1')])
                    elif _name == 'Card':
                        instance = obj(title='Test Card')
                    elif _name == 'Modal':
                        instance = obj(title='Test Modal')
                    elif _name == 'Navbar':
                        instance = obj(brand='Test Navbar')
                    else:
                        # Intenta con argumentos mínimos para otros componentes
                        try:
                            instance = obj()
                        except TypeError:
                            instance = obj(id='test')
                    
                    # Verifica que la instancia se creó correctamente
                    assert instance is not None, f"Failed to create instance of {_name}"
                    
            except Exception as e:
                failures.append((f"{modname}.{_name}", 'init', repr(e)))
    
    assert not failures, failures

if __name__ == '__main__':
    try:
        test_advanced_components()
        print('test_advanced_components: OK')
    except AssertionError as e:
        print('test_advanced_components: FAIL', e)
        sys.exit(1)