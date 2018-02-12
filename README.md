# Lazy Unit Tester
A tool to create unit test stubs from the functions inside the file you point it at.

The tool is designed to work on both Windows and Linux. However for ease, this project's unit tests are designed to run in the Vagrant environment included.


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

def MyFunction3():
    pass

def myfunction4():
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


class MyFunction3(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


class Myfunction4(unittest.TestCase):

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


## TODO:
+ Look into making it a plugin for SublimeText