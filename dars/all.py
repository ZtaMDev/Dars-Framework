# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
# Barrel import for all Dars components and core modules
# Usage: from dars.all import *

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
from dars.dars_tests.run_tests import run_app_tests, run_unit_tests, main
# Exporters (optional, for direct use)
from dars.exporters.web.html_css_js import HTMLCSSJSExporter
# Script utilities
from dars.scripts.dscript import dScript, RawJS, Arg
from dars.scripts.utils_ds import showModal, hideModal, goTo, goToNew, reload, goBack, goForward, alert, confirm, log, getDateTime, show, hide, toggle, addClass, removeClass, toggleClass, scrollTo, scrollToTop, scrollToBottom, scrollToElement, submitForm, resetForm, getValue, clearInput, saveToLocal, loadFromLocal, removeFromLocal, clearLocalStorage, copyToClipboard, copyElementText, focus, blur, setText, setTimeout, getInputValue, switch
from dars.scripts.animations import fadeIn, fadeOut, slideIn, slideOut, scaleIn, scaleOut, shake, bounce, pulse, rotate, flip, colorChange, morphSize, popIn, popOut, sequence  # Animation System
from dars.scripts.script import *
# Hooks
from dars.hooks import useDynamic
from dars.hooks.use_watch import useWatch
from dars.hooks.use_value import useValue
from dars.hooks.value_helpers import V, url, transform
from dars.hooks.form_helpers import FormData, collect_form
from dars.hooks.set_vref import setVRef
from dars.hooks.update_vref import updateVRef
# KeyCode for keyboard events
from dars.scripts.keycode import KeyCode, onKey, addGlobalKeys
from dars.version import __version__

# Backend HTTP Utilities (complete import)
from dars.backend.http import fetch, get, post, put, delete, patch
from dars.backend.data import useData, DataAccessor
from dars.backend.json_utils import stringify, parse, get_value
from dars.backend.components import createComp, updateComp, deleteComp

# Server Components (use_server=True)
from dars.core.server_components import (
    ServerComponentMarker,
    register_server_component,
    clear_server_component_registry,
    get_server_component,
    SERVER_COMPONENT_REGISTRY
)

# from dars.core.properties import *

__all__ = [
    'App', 'Component', 'EventManager',
    'Button', 'Checkbox', 'Container', 'DatePicker', 'Image', 'Input', 'Link', 'Page', 'ProgressBar',
    'RadioButton', 'Select', 'Slider', 'Spinner', 'Text', 'Textarea', 'Tooltip',
    'Accordion', 'Card', 'Modal', 'Navbar', 'Table', 'Tabs', 'Section', 'Outlet', 'Head', 'Audio', 'Video',
    'FileUpload',
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
    'useData', 'DataAccessor',
    'stringify', 'parse', 'get_value',
    'createComp', 'deleteComp', 'updateComp', 'RawJS', 'this', 'Arg', 'SelectOption', 
    # SPA Routing
    'route', 'SPARoute', 'RouteNode',
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
    'copyToClipboard', 'copyElementText',
    # Focus utilities
    'focus', 'blur',
    # Timer utilities
    'setTimeout',
    # Animation System
    'fadeIn', 'fadeOut', 'slideIn', 'slideOut', 'scaleIn', 'scaleOut',
    'shake', 'bounce', 'pulse', 'rotate', 'flip',
    'colorChange', 'morphSize', 'popIn', 'popOut', 'sequence',
    # Input utilities
    'getInputValue',
    # Hooks
    'useDynamic', 'useWatch',
    # useValue Hook
    'useValue', 'V', 'url', 'transform',
    # VRef Hooks
    'setVRef', 'updateVRef',
    # KeyCode for keyboard events
    'KeyCode', 'onKey', 'addGlobalKeys', 'switch',
    # Form utilities
    'FormData', 'collect_form',
    # Secure Routing
    'RouteType', 'RouteMetadata',
    # Server Components
    'ServerComponentMarker', 'register_server_component', 
    'clear_server_component_registry', 'get_server_component', 'SERVER_COMPONENT_REGISTRY',
]
