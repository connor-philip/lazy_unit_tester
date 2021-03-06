# Lazy Unit Tester
[![Build Status](https://travis-ci.org/connor-philip/lazy_unit_tester.svg?branch=master)](https://travis-ci.org/connor-philip/lazy_unit_tester)

A tool to create unit test stubs from the functions inside the file you point it at.

The tool is designed to work on both Windows and Linux.


 ---


## Usage
**Syntax:**

**`python lazy.py -f FILE [-d] [-i] [-c]`**

| Parameter | Description |
------------|--------------
| -f        | Target file to create tests for.  |
| -d        | Target directory to create tests. Default is target_file_directory/tests/ |
| -i        | Include indented functions        |
| -c        | Include commented functions       |
| -h        | Prints basic help menu            |



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