# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
import json
import os
from typing import Tuple, Dict, Any

DEFAULT_CONFIG = {
    "entry": "main.py",
    "format": "web",
    "outdir": "dist",
    "publicDir": None,  # autodetect if None: prefers ./public then ./assets
    "include": [],
    "exclude": ["**/__pycache__", ".git", ".venv", "node_modules"],
    "bundle": True,
    "defaultMinify": True,
    "viteMinify": True,
    "markdownHighlight": True,
    "markdownHighlightTheme": "auto",
    "targetPlatform": "auto",  # Desktop-only option: platform target for Electron build (auto|windows|linux|macos)
    # Optional: backend entry for SSR projects (module or file path). Disabled by default.
    "backendEntry": None,
    # Optional: custom utility styles map consumed by register_custom_utilities
    "utility_styles": {},
}

CONFIG_FILENAME = "dars.config.json"


def load_config(project_root: str) -> Tuple[Dict[str, Any], bool]:
    """Load dars.config.json from project_root. Returns (config, found)."""
    config_path = os.path.join(project_root, CONFIG_FILENAME)
    if not os.path.isfile(config_path):
        # Autodetect public dir if exists for convenience even without config
        cfg = DEFAULT_CONFIG.copy()
        if os.path.isdir(os.path.join(project_root, "public")):
            cfg["publicDir"] = "public"
        elif os.path.isdir(os.path.join(project_root, "assets")):
            cfg["publicDir"] = "assets"
        return cfg, False
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        cfg = DEFAULT_CONFIG.copy()
        cfg.update({k: v for k, v in data.items() if v is not None})
        return cfg, True
    except Exception:
        # On parse error, fallback to defaults but mark as not found to avoid enforcing
        cfg = DEFAULT_CONFIG.copy()
        return cfg, False


def resolve_paths(cfg: Dict[str, Any], project_root: str) -> Dict[str, Any]:
    """Return a copy of cfg with absolute resolved paths for entry, publicDir, outdir."""
    out = dict(cfg)
    if out.get("entry"):
        out["entry_abs"] = os.path.join(project_root, out["entry"])
    else:
        out["entry_abs"] = None
    if out.get("publicDir"):
        out["public_abs"] = os.path.join(project_root, out["publicDir"])
    else:
        # If None, keep None; exporter may still auto-detect
        out["public_abs"] = None
    if out.get("outdir"):
        out["outdir_abs"] = os.path.join(project_root, out["outdir"])
    else:
        out["outdir_abs"] = os.path.join(project_root, "dist")
    return out


def copy_public_dir(public_dir: str, dest_dir: str, include=None, exclude=None):
    """Copy entire public_dir into dest_dir applying basic include/exclude filters.
    Exclude supports substrings or glob-like simple matches; keep it simple to avoid heavy deps.
    """
    import shutil
    from pathlib import Path

    if not public_dir or not os.path.isdir(public_dir):
        return

    include = include or []
    exclude = exclude or []

    def is_excluded(path: Path) -> bool:
        # Simple checks: substring or name matches
        p_str = str(path)
        for pat in exclude:
            if pat in p_str:
                return True
        return False

    def is_included(path: Path) -> bool:
        if not include:
            return True
        p_str = str(path)
        for pat in include:
            if pat in p_str:
                return True
        return False

    for root, dirs, files in os.walk(public_dir):
        # filter excluded dirs in-place
        dirs[:] = [d for d in dirs if not is_excluded(Path(root) / d)]
        for f in files:
            src_path = Path(root) / f
            if is_excluded(src_path) or not is_included(src_path):
                continue
            rel = src_path.relative_to(public_dir)
            dst_path = Path(dest_dir) / rel
            os.makedirs(dst_path.parent, exist_ok=True)
            try:
                shutil.copy2(str(src_path), str(dst_path))
            except Exception:
                # Best-effort; ignore copy errors
                pass


def write_default_config(project_root: str, overwrite: bool = False) -> str:
    """Create a dars.config.json with defaults if it doesn't exist (or overwrite=True).
    Returns the path to the config file.
    """
    path = os.path.join(project_root, CONFIG_FILENAME)
    if os.path.exists(path) and not overwrite:
        return path
    cfg = DEFAULT_CONFIG.copy()
    # Prefer autodetected public dir as default
    if os.path.isdir(os.path.join(project_root, "public")):
        cfg["publicDir"] = "public"
    elif os.path.isdir(os.path.join(project_root, "assets")):
        cfg["publicDir"] = "assets"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    return path


def update_config(project_root: str, updates: Dict[str, Any]) -> str:
    """Update or create config merging with defaults.
    Returns the path to the config file.
    """
    cfg, _ = load_config(project_root)
    cfg.update({k: v for k, v in updates.items() if v is not None})
    path = os.path.join(project_root, CONFIG_FILENAME)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    return path
