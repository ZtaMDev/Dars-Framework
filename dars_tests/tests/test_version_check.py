import importlib, sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dars'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
import dars.version as ver

# Latest version observed on PyPI / mirrors during analysis: 1.1.3
LATEST_KNOWN = '1.1.3'

def test_version_comparison():
    local = getattr(ver, '__version__', None)
    assert local is not None, 'local version not found in dars.version'
    print(f'local_version={local}; latest_known={LATEST_KNOWN}')
    # The test will not fail if local is newer (dev), but will warn via printing when local differs.
    if local != LATEST_KNOWN:
        print('WARNING: local package version differs from LATEST_KNOWN (see test output).')
    else:
        print('version_check: OK')

if __name__ == '__main__':
    test_version_comparison()
