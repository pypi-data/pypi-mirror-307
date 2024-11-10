import os.path

from chinu9653s.src.decorator.warning.not_used_return_value import use_return


@use_return
def a():
    return "10"

print(a())
print(os.path.join("a", a()))