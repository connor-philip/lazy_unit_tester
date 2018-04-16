# Lazy Unit Tester
[![Build Status](https://travis-ci.org/connor-philip/lazy_unit_tester.svg?branch=master)](https://travis-ci.org/connor-philip/lazy_unit_tester)

A tool to create unit test stubs from the functions inside the file you point it at.

The tool is designed to work on both Windows and Linux.


 ---


## Usage
**Syntax:**

**`python lazy.py -f FILE [-i] [-c]`**

| Parameter | Description |
------------|--------------
| -f        | Target file to create tests for. Required    |
| -i        | Include indented functions                   |
| -c        | Include commented functions                  |
| -h        | Prints basic help menu                       |



## Example

`python lazy.py -f C:\project\my_functions.py`
```python
def my_function1():
    pass

def myFunction2():
    pass

def another_function ():
    pass

```
**Should create:**

`C:\project\tests\test_my_functions.py`
```python
import unittest
import my_functions.


class MyFunction1(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


class MyFunction2(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


class AnotherFunction(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()

```


## Note
This tool is designed to work for python files, and the default python unittest package. I don't have any plans myself to add support in terms of new unittesting packages, or languages. However if anyone wishes to contribute, I'm more than happy to accept any reviewed changes to add more support, and to help change the current functionality also.