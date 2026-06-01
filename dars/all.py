# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
# Barrel import for all Dars components and core modules
# Usage: from dars.all import *
"""## Barrel Import

You can import all main components and modules with a single line:

```python
from dars.all import *
```

This simplifies integration and improves developer experience by exposing components like `Text`, `Button`, `Container`, `State`, and DAP functions like `log`, `alert`, `showModal`, etc."""
# Advanced Components
from dars.components.advanced.accordion import Accordion
from dars.components.advanced.card import Card
from dars.components.advanced.modal import Modal
from dars.components.advanced.navbar import Navbar
from dars.components.advanced.table import Table
from dars.components.advanced.tabs import Tabs
# Visualization Components
from dars.components.visualization.chart import Chart
from dars.components.visualization.table import DataTable
# Basic Components
from dars.components.basic.button import Button
from dars.components.basic.checkbox import Checkbox
from dars.components.basic.container import Container
from dars.components.basic.datepicker import DatePicker
from dars.components.basic.image import Image
from dars.components.basic.input import Input
from dars.components.basic.link import Link
from dars.components.basic.markdown import Markdown
from dars.components.basic.page import Page
from dars.components.basic.progressbar import ProgressBar
from dars.components.basic.radiobutton import RadioButton
from dars.components.basic.select import Select, SelectOption
from dars.components.basic.slider import Slider
from dars.components.basic.spinner import Spinner
from dars.components.basic.text import Text
from dars.components.basic.textarea import Textarea
from dars.components.basic.tooltip import Tooltip
from dars.components.layout.anchor import AnchorPoint
from dars.components.layout.flex import FlexLayout
from dars.components.basic.section import Section
from dars.components.advanced.head import Head
from dars.components.advanced.outlet import Outlet
from dars.components.basic.video import Video
from dars.components.basic.audio import Audio
from dars.components.advanced.file_upload import FileUpload
# Conditional & list rendering helpers
from dars.components.basic.show_component import Show_Component as Show
from dars.components.basic.each_component import Each_Component as Each
# Layout
from dars.components.layout.grid import GridLayout, LayoutBase
# Core
from dars.core.app import App
from dars.core.component import Component, FunctionComponent, Props
from dars.core.events import EventHandler, EventEmitter, EventManager
from dars.core.events import EventManager
from dars.core.events import EventTypes
from dars.core.routing import route, SPARoute, RouteNode  # SPA Routing
from dars.core.route_types import RouteType, RouteMetadata  # Secure Routing
# CLI (optional, for advanced usage)
# from dars.cli.main import main as dars_cli_main
# State Management
from dars.core.state import dState, Mod, this, this_for  # Legacy (backward compatibility)
from dars.core.state_v2 import State, ReactiveProperty, StateTransition  # V2 State System (PRIMARY)
from dars.core.auth import DarsAuth, requires_auth, requires_role  # Core Auth Module
from dars.dars_tests.run_tests import run_app_tests, run_unit_tests, main
# Exporters (optional, for direct use)
from dars.exporters.web.html_css_js import HTMLCSSJSExporter
# Script utilities
from dars.scripts.dscript import dScript, RawJS, Arg
from dars.scripts.utils_ds import showModal, hideModal, goTo, goToNew, reload, goBack, goForward, alert, confirm, log, getDateTime, show, hide, toggle, addClass, removeClass, toggleClass, scrollTo, scrollToTop, scrollToBottom, scrollToElement, submitForm, resetForm, getValue, clearInput, saveToLocal, loadFromLocal, removeFromLocal, clearLocalStorage, copyToClipboard, copyElementText, focus, blur, setText, setTimeout, getInputValue, switch, runSequence, setHtml, redirect_after_login, navigate_to
from dars.scripts.utils_ds import onViewport, classOnView, runOnView, animateOnView, staggerOnView, scrollProgress, animate, timeline, stagger # Viewport & Scroll Animation Utilities
from dars.scripts.animations import fadeIn, fadeOut, slideIn, slideOut, scaleIn, scaleOut, shake, bounce, pulse, rotate, flip, colorChange, morphSize, popIn, popOut, sequence  # Animation System
from dars.scripts.script import *
# Hooks
from dars.hooks import useDynamic
from dars.hooks.use_watch import useWatch
from dars.hooks.use_value import useValue
from dars.hooks.value_helpers import V, url, transform
from dars.hooks.form_helpers import FormData, collect_form
from dars.hooks.set_vref import setVRef
from dars.hooks.update_vref import updateVRef, updateVRefFromResponse
from dars.hooks.use_fetch import useFetch
from dars.hooks.form_validator import (
    FormValidator,
    required, min_length, max_length, pattern, email, min_value, max_value, custom,
)
# KeyCode for keyboard events
from dars.scripts.keycode import KeyCode, onKey, addGlobalKeys
from dars.version import __version__

# Backend HTTP Utilities (complete import)
from dars.backend.http import fetch, get, post, put, delete, patch
from dars.backend.http import add_request_interceptor, add_response_interceptor, clear_interceptors, use_auth_interceptor
from dars.backend.data import useData, DataAccessor
from dars.backend.json_utils import stringify, parse, get_value
from dars.backend.components import createComp, updateComp, deleteComp
from dars.backend.store import JsonStore
from dars.backend.middleware import SecurityHeadersMiddleware, AuthMiddleware, CORSMiddleware, RateLimitMiddleware, LoggingMiddleware, CompressionMiddleware, DarsMiddleware
from dars.backend.upload import UploadPipeline
from dars.backend.actions import server_action, call_server
from dars.backend.database import Database
from dars.backend.models import DarsModel, IntegerField, TextField, FloatField, BooleanField, DateTimeField, JSONField, ForeignKey, ModelManager, register_model_api
from dars.hooks.use_vref import useVRef


# from dars.core.properties import *

__all__ = [
    'App', 'Component', 'EventManager',
    'Button', 'Checkbox', 'Container', 'DatePicker', 'Image', 'Input', 'Link', 'Page', 'ProgressBar',
    'RadioButton', 'Select', 'Slider', 'Spinner', 'Text', 'Textarea', 'Tooltip',
    'Accordion', 'Card', 'Modal', 'Navbar', 'Table', 'Tabs', 'Section', 'Outlet', 'Head', 'Audio', 'Video',
    'FileUpload',
    # Conditional & list rendering
    'Show', 'Each',
    # Visualization
    'Chart', 'DataTable',
    'GridLayout', 'FlexLayout', 'LayoutBase', 'AnchorPoint',
    'InlineScript', 'FileScript', 'dScript', 'HTMLCSSJSExporter',
    'EventTypes', 'EventHandler', 'EventEmitter', 'EventManager', 'Markdown',
    '__version__', 'FunctionComponent', 'Props',
    'run_app_tests', 'run_unit_tests', 'main',
    # State Management V2 (PRIMARY)
    'State', 'ReactiveProperty', 'StateTransition',
    # Legacy State Management (backward compatibility)
    'dState', 'Mod', 'this_for',
    # Backend HTTP Utilities
    'fetch', 'get', 'post', 'put', 'delete', 'patch',
    'add_request_interceptor', 'add_response_interceptor', 'clear_interceptors', 'use_auth_interceptor',
    'useData', 'DataAccessor',
    'stringify', 'parse', 'get_value',
    'createComp', 'deleteComp', 'updateComp', 'RawJS', 'this', 'Arg', 'SelectOption',
    # Backend utilities
    'JsonStore', 'SecurityHeadersMiddleware', 'UploadPipeline',
    # SPA Routing
    'route', 'SPARoute', 'RouteNode',
    # Data Layer
    'Database', 'DarsModel', 'IntegerField', 'TextField', 'FloatField', 'BooleanField',
    'DateTimeField', 'JSONField', 'ForeignKey', 'ModelManager', 'register_model_api',
    # Server Actions
    'server_action', 'call_server',
    # Middleware
    'AuthMiddleware', 'CORSMiddleware', 'RateLimitMiddleware', 'LoggingMiddleware',
    'CompressionMiddleware', 'DarsMiddleware',
    # Modal utilities
    'showModal', 'hideModal',
    # Navigation utilities
    'goTo', 'goToNew', 'reload', 'goBack', 'goForward',
    # Alert & console utilities
    'alert', 'confirm', 'log', 'getDateTime',
    # DOM manipulation utilities
    'show', 'hide', 'toggle', 'addClass', 'removeClass', 'toggleClass', 'setText',
    # Scroll utilities
    'scrollTo', 'scrollToTop', 'scrollToBottom', 'scrollToElement',
    # Form utilities
    'submitForm', 'resetForm', 'getValue', 'clearInput',
    # Storage utilities
    'saveToLocal', 'loadFromLocal', 'removeFromLocal', 'clearLocalStorage',
    # Clipboard utilities
    'copyToClipboard', 'copyElementText',    # Focus utilities
    'focus', 'blur',
    # Timer utilities
    'setTimeout',
    # Animation System
    'fadeIn', 'fadeOut', 'slideIn', 'slideOut', 'scaleIn', 'scaleOut',
    'shake', 'bounce', 'pulse', 'rotate', 'flip',
    'colorChange', 'morphSize', 'popIn', 'popOut', 'sequence',
    # Viewport & Scroll Animation Engine
    'onViewport', 'classOnView', 'runOnView', 'animateOnView',
    'staggerOnView', 'scrollProgress', 'animate', 'timeline', 'stagger',
    # Input utilities
    'getInputValue',
    # Hooks
    'useDynamic', 'useWatch',
    # useValue Hook
    'useValue', 'V', 'url', 'transform',
    # VRef Hooks
    'setVRef', 'updateVRef', 'updateVRefFromResponse', 'useVRef',
    # KeyCode for keyboard events
    'KeyCode', 'onKey', 'addGlobalKeys', 'switch',
    # Form utilities
    'FormData', 'collect_form',
    # Form validation
    'FormValidator', 'required', 'min_length', 'max_length', 'pattern',
    'email', 'min_value', 'max_value', 'custom',
    # useFetch hook
    'useFetch', "runSequence", "setHtml", "redirect_after_login", "navigate_to",
    # Secure Routing
    'RouteType', 'RouteMetadata',
    # Auth System
    'DarsAuth', 'requires_auth', 'requires_role',
]
