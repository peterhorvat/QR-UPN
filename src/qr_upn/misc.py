import re


def control_number(column):
    ponders = [i for i in range(len([*column]) + 1, 1, -1)]
    result = 11 - (sum([a * b for a, b in zip(map(int, [*column]), ponders)]) % 11)
    if result == 10:
        return 0
    return result


def sum_multi(column):
    ponders = [i for i in range(len([*column]) + 1, 1, -1)]
    return sum([a * b for a, b in zip(map(int, [*column]), ponders)])


# MODEL 11 CHECKSUM CALCULATION
def model11_checksum(columns):
    last = int(columns[-1])
    result = 11 - (sum_multi(columns[:-1]) % 11)
    if result == 10 or result == 11:
        result = 0
    return result == last


def check_name(name):
    if not name.endswith('.png') or not name.endswith('.jpg') or not name.endswith('.jpeg'):
        return f"{name}.png"
    return name


def clean_str(s):
    return re.sub(r'[\n\t\s]*', '', s)
