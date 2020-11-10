# https://spyhce.com/blog/understanding-new-and-init
"""
__new__ and __init__
"""
class A():
    """
    1. __new__ handles object creation and __init__ handles object initialization
    2. __new__ accepts cls as it's first parameter and __init__ accepts self,
        because when calling __new__ you actually don't have an instance yet,
        whereas __init__ is called after __new__ and the instance is in place
    3.
    """
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, abc):
        self.abc = abc

def main():
    a = A()
    print(a)

main()