def coord_converter(x, y):
    x = x - 2
    if (0 <= y) and (y < 2):
        y = 2 + y
    else:
        y = 2 - y
    return x, y
