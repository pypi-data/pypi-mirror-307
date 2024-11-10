<!---
The MIT License (MIT)

Copyright (c) 2024 Almaz Ilaletdinov <a.ilaletdniov@yandex.ru>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
--->

# flake8-one-class

[![test](https://github.com/blablatdinov/flake8-one-class/actions/workflows/test.yml/badge.svg)](https://github.com/blablatdinov/flake8-one-class/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/blablatdinov/flake8-one-class/branch/master/graph/badge.svg)](https://codecov.io/gh/blablatdinov/flake8-one-class)
[![Python Version](https://img.shields.io/pypi/pyversions/flake8-one-class.svg)](https://pypi.org/project/flake8-one-class/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

## Background

In Python modules, having multiple classes in a single file can often indicate overly complex code or an unclear separation of concerns. The flake8-one-class plugin enforces a single public class per module to encourage modular and maintainable code design. Private (internal) classes are allowed but are intended for module-level encapsulation only.

## Installation

Install flake8-one-class using pip:

```
pip install flake8-one-class
```

## Usage

After installation, flake8-one-class will automatically run with flake8:

```
flake8 your_project_directory
```

This plugin checks each module for multiple public class definitions. If more than one public class is detected, an error is raised.

## Example

Given the following Python code:

```python
class Animal:
    pass

class Plant:
    pass
```

Running flake8 will produce the following error:

```
your_file.py:1:1: FOC100 found module with more than one public class
```

Using only one public class in the module will resolve the error:

```python
class Animal:
    pass

class _Helper:  # private class is allowed
    pass
```


## License

[MIT](https://github.com/blablatdinov/flake8-one-class/blob/master/LICENSE)


## Credits

This project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [9899cb192f754a566da703614227e6d63227b933](https://github.com/wemake-services/wemake-python-package/tree/9899cb192f754a566da703614227e6d63227b933). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/9899cb192f754a566da703614227e6d63227b933...master) since then.
