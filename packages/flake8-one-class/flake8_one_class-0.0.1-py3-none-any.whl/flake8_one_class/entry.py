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

from collections.abc import Generator
from typing import final

from flake8_one_class.visitor import ModuleVisitor


@final
class Plugin:
    """Flake8 plugin."""

    def __init__(self, tree) -> None:
        """Ctor."""
        self._tree = tree

    def run(self) -> Generator[tuple[int, int, str, type], None, None]:
        """Entry."""
        visitor = ModuleVisitor()
        visitor.visit(self._tree)
        for _ in visitor.problems:  # noqa: WPS526
            yield (1, 0, 'FOC100 found module with more than one public class', type(self))
