# x-strings
![PyPI - Version](https://img.shields.io/pypi/v/x-strings)
![PyPI - License](https://img.shields.io/pypi/l/x-strings)
![PyPI - Downloads](https://img.shields.io/pypi/dm/x-strings)

Extend Python syntax by defining custom string prefix. Provide function that transforms strings with your prefix.

This corresponds to Tagged Template Literals feature in JavaScript.

This project is only a toy. Technique used here shouldn't be considered as a good coding practice due to the fact how it is implemented. I don't recommend using it in production code. Hopefully it can be inspiring though.

## Features

- Multiple encodings can be defined
- Multiple prefixes can be defined
- Prefixes can have more that one letter
- Encodings can take arguments (captured by regex)
- Doesn't corrupt Python syntax-error messages

## Examples

Simple example is shown below.

`app.py`:

```python
# coding: x-strings
print(x"Hello World")
```

`launcher.py`:

```python
import xstrings
xstrings.register({'x': lambda t: t + "!!!"})

import app
```

Notice exclamation marks added to the end of the message:
```sh
$ python3 -B examples/launcher.py
Hello World!!!
```

This and more advanced examples can be found in [here](https://github.com/gergelyk/xstrings/tree/master/examples).

## Caching

By default Python stores decoded code in `__pycache__`. Source file needs to be changed to get cache re-generated. This may complicate development of `launcher.py`. You can prevent Python from generating cache by either:

- Setting env var: `PYTHONDONTWRITEBYTECODE` to `1`
- Using `-B` switch for `python`
- Calling `sys.dont_write_bytecode = True` in the code

## References

Project is inspired by [pyxl4](https://github.com/pyxl4/pyxl4).
