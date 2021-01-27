
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

color_codes = {
    '&0': 'Black',
    '&1': 'Red',
    '&2': 'Green',
    '&3': 'Yellow',
    '&4': 'Blue',
    '&5': 'Magenta',
    '&6': 'Cyan',
    '&7': 'White',
    '&8': 'Reset',
}


def assert_err(test_name):
    assert False, cstring(
        f"&3Test &1{test_name} failed!")


def assert_success(test_name):
    print(color_string(f"Test {test_name} PASSED!", 'Green'))


def do_assert(test_name, output, expected):
    assert output == expected, cstring(
        f"&1Test {test_name} failed: output &3{output}&1 expected to be &3{expected}")
    print(cstring(f"&2Test &5{test_name}&2 PASSED!"))


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


def cstring(s):
    s += "&8  "
    ac = 0
    for c in range(len(s)):
        x = c+ac
        if s[x] == "&" and s[x-1] != "\\":
            ac += len(colors[color_codes[s[x:x+2]]])-2
            s = s[:x] + colors[color_codes[s[x:x+2]]] + s[x+2:]
    return s
