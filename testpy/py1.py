from typing import Callable


def func2(*args: str)->Callable:
    """This is annotation function"""

@func2
def func1():
    """This is a test function
this is second line of the func"""
    print("test1")
    return "test"

print(func2.__name__)
print(func1.__doc__)