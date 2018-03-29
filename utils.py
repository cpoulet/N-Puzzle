###############################################################################
#            _   _        _____  _    _ _____________      ______             #
#           | \ | |      |  __ \| |  | |___  /___  / |    |  ____|            #
#           |  \| |______| |__) | |  | |  / /   / /| |    | |__               #
#           | . ` |______|  ___/| |  | | / /   / / | |    |  __|              #
#           | |\  |      | |    | |__| |/ /__ / /__| |____| |____             #
#           |_| \_|      |_|     \____//_____/_____|______|______|            #
#                                                                             #
###############################################################################

def get_snake(size):
    if size < 2:
        return []
    total_size = size * size
    grid = [-1 for i in range(total_size)]
    current = 1
    x = 0
    ix = 1
    y = 0
    iy = 0
    while current != 0:
        grid[x + y * size] = current
        current += 1
        if x + ix == size or x + ix < 0 or (ix != 0 and grid[x + ix + y * size] != -1):
            iy = ix
            ix = 0
        elif y + iy == size or y + iy < 0 or (iy != 0 and grid[x + (y + iy) * size] != -1):
            ix = -iy
            iy = 0
        x += ix
        y += iy
        if current == size * size:
            current = 0
            grid[x + y * size] = current
    return grid

def locate(user_string, x=0, y=0):
	HORIZ=str(int(x))
	VERT=str(int(y))
	print("\033[" + VERT + ";" + HORIZ + "f" + user_string)

def get_sqrts(n):
    ret = {}
    for i in range(n):
        ret[i * i] = i
    return ret

def pos(nb, size):
    return (nb // size, nb % size)

def ltok(li):
    return ''.join([chr(x) for x in li])

def ktol(key):
    return [ord(x) for x in key]

NBR = 25

snake = [get_snake(i) for i in range(NBR)]
sqrt = get_sqrts(NBR)
