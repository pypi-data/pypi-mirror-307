# The MIT License (MIT)
#
# Copyright (c) 2024 Almaz Ilaletdinov <a.ilaletdniov@yandex.ru>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

import ast
from typing import final


@final
class ModuleVisitor(ast.NodeVisitor):
    """Class visitor for checking class count in module."""

    def __init__(self) -> None:
        """Ctor."""
        self.problems: list[int] = []

    def visit_Module(self, node) -> None:  # noqa: N802, WPS231, C901. Flake8 plugin API
        """Visit by modules."""
        classes_count = 0
        for elem in node.body:
            if isinstance(elem, ast.ClassDef) and not elem.name.startswith('_'):
                classes_count += 1
            if classes_count > 1:
                self.problems.append(1)
        self.generic_visit(node)
