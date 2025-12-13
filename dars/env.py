# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev

# Dars Framework - Environment Variables
#
# This file provides the DarsEnv class to handle environment-specific logic.

class DarsEnv:
    """
    Environment configuration for Dars Framework.
    
    Attributes:
        dev (bool): Indicates if the application is running in development mode.
                    True by default (interactive/dev), False when exported for production (bundle=True).
    """
    dev = True

    @classmethod
    def set_dev_mode(cls, is_dev: bool):
        """Set the development mode flag."""
        cls.dev = is_dev
