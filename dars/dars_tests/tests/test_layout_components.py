import importlib, inspect, sys, os
from dars.core.component import Component

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dars'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

failures = []

def test_layout_components():
    base_pkg = 'dars.components.layout'
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
                    # Intenta crear una instancia con argumentos mínimos
                    try:
                        instance = obj()
                    except TypeError:
                        try:
                            instance = obj(id='test')
                        except Exception as e:
                            failures.append((f"{modname}.{_name}", 'init', repr(e)))
                    
                    # Verifica que la instancia se creó correctamente
                    if 'instance' in locals():
                        assert instance is not None, f"Failed to create instance of {_name}"
                    
            except Exception as e:
                failures.append((f"{modname}.{_name}", 'inspect', repr(e)))
    
    assert not failures, failures

if __name__ == '__main__':
    try:
        test_layout_components()
        print('test_layout_components: OK')
    except AssertionError as e:
        print('test_layout_components: FAIL', e)
        sys.exit(1)