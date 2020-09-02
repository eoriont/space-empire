
colors = {
    'Black': '\u001b[30m',
    'Red': '\u001b[31m',
    'Green': '\u001b[32m',
    'Yellow': '\u001b[33m',
    'Blue': '\u001b[34m',
    'Magenta': '\u001b[35m',
    'Cyan': '\u001b[36m',
    'White': '\u001b[37m',
    'Reset': '\u001b[0m',
}


def assert_err(test_name):
    assert False, color_string(
        f"Test {test_name} failed!", 'Red')


def assert_success(test_name):
    print(color_string(f"Test {test_name} PASSED!", 'Green'))


def do_assert(test_name, output, expected):
    assert output == expected, color_string(
        f"Test {test_name} failed: output {output} expected to be {expected}", 'Red')
    print(color_string(f"Test {test_name} PASSED!", 'Green'))


def assert_bool(test_name, boolean):
    assert boolean, color_string(
        f"Test {test_name} failed! Check the code to see the problem!", 'Red')
    print(color_string(f"Test {test_name} PASSED!", 'Green'))


def assert_exception(test_name, func, *args):
    try:
        func(*args)
    except Exception:
        print(color_string(f'Test {test_name} PASSED!', 'Green'))
        return
    raise Exception(
        color_string(f"Test {test_name} failed because it didn't throw an exception!", 'Red'))


def color_print(s, col):
    print(color_string(s, col))


def color_string(s, col):
    return f"{colors[col]}{s}{colors['Reset']}"
