from src.chinus.decorator.warning.not_used_return_value import use_return


@use_return
def a():
    pass

a()
x = a()
print(a())