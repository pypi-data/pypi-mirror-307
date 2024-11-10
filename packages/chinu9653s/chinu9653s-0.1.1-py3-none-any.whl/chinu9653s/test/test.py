import os.path

from chinu9653s.src.decorator.warning.not_used_return_value import use_return
from chinu9653s.src.tools.paths.get.absolute_path import get_absolute_path


import sys
from functools import wraps

@use_return
def a():
    return "10"
if a():
    print(1)

# print(type(get_absolute_path("10")))