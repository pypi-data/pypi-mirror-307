from src.chinus.decorator.warning.not_used_return_value import use_return


def br_print(*lines):
    for line in lines:
        print(line)



@use_return
def br_input(*lines, prompt=None):
    br_print(*lines)
    return input(prompt)