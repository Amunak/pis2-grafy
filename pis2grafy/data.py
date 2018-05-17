import re

data = [
    """Node       1   2    3   4    5    6
    1             0   8    0   2    7    3
    2             0   0    2   4    0    8
    3             0   0    0   6    18   12
    4             0   0    0   0    8    3
    5             0   0    0   0    0    6
    6             0   0    0   0    0    0 """,
]


def parse_raw(number, skip_first_line=True, skip_first_column=True):
    matrix = []
    raw_data = data[number].strip()

    lines = raw_data.split('\n')
    if skip_first_line is True:
        lines.pop(0)

    for line in lines:
        words = re.split('\s+', line.strip())
        if skip_first_column is True:
            words.pop(0)
        matrix.append([int(word.strip()) for word in words])

    return matrix


def parse_all():
    return [parse_raw(index) for index, raw_data in enumerate(data)]
