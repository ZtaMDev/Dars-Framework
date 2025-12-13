import json, os, sys
from datetime import datetime
from typing import Any, Dict, Tuple

APP_NAME = "Dars"


def _config_base_dir() -> str:
    # Windows
    if os.name == 'nt':
        base = os.getenv('APPDATA') or os.path.expanduser('~')
        return os.path.join(base, APP_NAME)
    # POSIX
    xdg = os.getenv('XDG_CONFIG_HOME')
    if xdg:
        return os.path.join(xdg, 'dars')
    return os.path.join(os.path.expanduser('~/.config'), 'dars')


def get_config_path() -> str:
    d = _config_base_dir()
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, 'config.json')


def load_config() -> Dict[str, Any]:
    p = get_config_path()
    if not os.path.isfile(p):
        return {
            'requirements': {
                'node': {'ok': False, 'version': None, 'source': None, 'checked_at': None},
                'bun': {'ok': False, 'version': None, 'source': None, 'checked_at': None},
                'optional': {}
            },
            'python_deps': {'ok': True, 'missing': [], 'checked_at': None},
            'satisfied': False,
            'last_doctor': None,
        }
    try:
        with open(p, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {
            'requirements': {
                'node': {'ok': False, 'version': None, 'source': None, 'checked_at': None},
                'bun': {'ok': False, 'version': None, 'source': None, 'checked_at': None},
                'optional': {}
            },
            'python_deps': {'ok': True, 'missing': [], 'checked_at': None},
            'satisfied': False,
            'last_doctor': None,
        }


def save_config(cfg: Dict[str, Any]) -> None:
    p = get_config_path()
    try:
        cfg['last_doctor'] = datetime.utcnow().isoformat() + 'Z'
    except Exception:
        pass
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, indent=2)
