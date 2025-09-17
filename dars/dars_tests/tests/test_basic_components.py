import importlib, inspect, sys, os
from dars.core.component import Component

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dars'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

failures = []

def test_basic_components():
    base_pkg = 'dars.components.basic'
    try:
        pkg = importlib.import_module(base_pkg)
    except Exception as e:
        failures.append((base_pkg, 'import', repr(e)))
        return
    
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
                    # Proporciona argumentos específicos para cada componente
                    if _name == 'Image':
                        instance = obj(src='test.png')
                    elif _name == 'Link':
                        instance = obj(text='Test', href='#')
                    elif _name == 'Markdown':
                        instance = obj(content='# Test')
                    elif _name == 'ProgressBar':
                        instance = obj(value=50)
                    elif _name == 'Tooltip':
                        from dars.components.basic.text import Text
                        instance = obj(text='Tip', child=Text('Hover me'))
                    elif _name == 'Button':
                        instance = obj(text='Test Button')
                    elif _name == 'Input':
                        instance = obj()
                    elif _name == 'Textarea':
                        instance = obj()
                    elif _name == 'Checkbox':
                        instance = obj(label='Test Checkbox')
                    elif _name == 'RadioButton':
                        instance = obj(label='Test Radio', name='test_radio')
                    elif _name == 'Select':
                        instance = obj(options=[{'value': 'test', 'label': 'Test'}])
                    elif _name == 'Slider':
                        instance = obj()
                    elif _name == 'DatePicker':
                        instance = obj()
                    elif _name == 'Container':
                        instance = obj()
                    elif _name == 'Text':
                        instance = obj(text='Test Text')
                    else:
                        # Intenta con argumentos mínimos para otros componentes
                        try:
                            instance = obj()
                        except TypeError:
                            instance = obj(id='test', class_name='c', style={})
                    
                    # Verifica que la instancia se creó correctamente
                    assert instance is not None, f"Failed to create instance of {_name}"
                    
            except Exception as e:
                failures.append((f"{modname}.{_name}", 'init', repr(e)))
    
    assert not failures, failures

if __name__ == '__main__':
    try:
        test_basic_components()
        print('test_basic_components: OK')
    except AssertionError as e:
        print('test_basic_components: FAIL', e)
        sys.exit(1)