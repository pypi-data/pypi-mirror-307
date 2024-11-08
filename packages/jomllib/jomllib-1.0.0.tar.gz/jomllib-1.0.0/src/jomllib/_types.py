# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileCopyrightText: 2024 Joe Clack
#
# The contents of this file are largely based upon 
# https://github.com/python/cpython/blob/9ab3d31b66c60fa2f67fcbc8744146bcb520a1b3/Lib/tomllib/_types.py
# Copyright © 2001-2024 Python Software Foundation. All rights reserved.
# PSF licenses the referenced content to Joe Clack under the terms of the PSF-2.0 license.
#
# Copyright 2021 Taneli Hukkinen
# Taneli Hukkinen licenses their work to the Python Software Foundation under the terms of the MIT license.

from typing import Any, Callable, Tuple

# Type annotations
ParseFloat = Callable[[str], Any]
Key = Tuple[str, ...]
Pos = int
