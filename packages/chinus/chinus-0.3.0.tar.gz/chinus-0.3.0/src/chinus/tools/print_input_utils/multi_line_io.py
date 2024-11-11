

def br_print(*lines):
    for line in lines:
        print(line)


def br_input(*lines, prompt=None):
    br_print(*lines)
    return input(prompt)