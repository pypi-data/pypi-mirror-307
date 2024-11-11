gamelib
=======

[![PyPI version](https://badge.fury.io/py/vtece4564-gamelib.svg)](https://badge.fury.io/py/vtece4564-gamelib)

This project provides a Python library teams may use for
satisfying various aspects of the final project for ECE 4564.
It contains the following packages:

* [gameauth](src/main/python/gameauth/README.md) -- authentication and authorization support
* [gamecomm](src/main/python/gamecomm/README.md) -- client and server communication support
* [gamedb](src/main/python/gamedb/README.md) -- user and game database support

Installation
------------

To install this library, update your project's `requirements.txt` to include
the name of the library.

```
vtece4564-gamelib
```

Then install the dependency either using your IDE or `pip`

* In PyCharm, simply opening the `requirements.txt` will notify you of any  
  missing dependencies and will offer you an opportunity to install, OR
* Use `pip install -r requirements.txt` while your project's virtual
  environment is active in your shell.

