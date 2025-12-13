import os
from typing import Any
from .persist import load_config, save_config
from .doctor import run_doctor


SKIP_COMMANDS = { 'doctor', 'forcedev' }


def check_and_gate(command: str) -> None:
    """
    Runs once before any CLI command (except 'doctor').
    If environment hasn't satisfied mandatory requirements, invoke doctor.
    After a successful run, future commands proceed without gating.
    """
    if command in SKIP_COMMANDS:
        return
    # Allow CI to skip interactivity but still fail properly
    if os.getenv('DARS_NO_PREFLIGHT') == '1':
        return

    cfg = load_config()
    if cfg.get('satisfied'):
        return

    # If not satisfied, run doctor interactively
    code = run_doctor(check_only=False, auto_yes=False, install_all=False, force=False)
    # If doctor returns non-zero, we still persist current state and let the caller decide to exit
    # but generally, the CLI will continue only if requirements are satisfied; we make it strict here
    cfg = load_config()
    if not cfg.get('satisfied'):
        # Propagate an exception to abort command execution
        raise SystemExit(1)
