# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
Dars Hooks System

Hooks provide a way to add reactive and stateful behavior to FunctionComponents.
"""

from .use_dynamic import useDynamic
from .form_helpers import FormData, collect_form
from .use_vref import useVRef
from .set_vref import setVRef
from .update_vref import updateVRef

__all__ = ['useDynamic', 'FormData', 'collect_form', 'useVRef', 'setVRef', 'updateVRef']
