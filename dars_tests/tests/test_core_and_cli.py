import importlib, sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dars'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def test_core_imports():
    import dars.core.app as app
    import dars.core.component as component
    import dars.cli.main as cli_main
    # smoke tests: ensure some expected names exist
    assert hasattr(app, 'App') or hasattr(app, 'Page'), 'app module missing App/Page'
    assert hasattr(component, 'Component'), 'component missing Component'
    assert hasattr(cli_main, 'main') or hasattr(cli_main, 'run'), 'cli main missing entrypoint'
    print('core_and_cli: OK')

if __name__ == '__main__':
    test_core_imports()
