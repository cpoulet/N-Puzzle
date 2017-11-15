###############################################################################
#            _   _        _____  _    _ _____________      ______             #
#           | \ | |      |  __ \| |  | |___  /___  / |    |  ____|            #
#           |  \| |______| |__) | |  | |  / /   / /| |    | |__               #
#           | . ` |______|  ___/| |  | | / /   / / | |    |  __|              #
#           | |\  |      | |    | |__| |/ /__ / /__| |____| |____             #
#           |_| \_|      |_|     \____//_____/_____|______|______|            #
#                                                                             #
###############################################################################

# Our modules

# Other modules
import collections
import bisect

class OrderedValueDict:
    '''Dictionnary with:
    O(1) :      pop()
                contain()
    O(log(n)) : insort()'''
    def __init__(self):
        self.d = {}
        self.list = collections.deque()
        self.lenmax = 0

    def insort(self, key, value, sort_val):
        self.d[key] = value
        bisect.insort(self.list, (sort_val, key))
        if len(self.list) > self.lenmax:
            self.lenmax += 1

    def contain(self, key):
        return self.d.get(key)

    def pop(self):
        key = self.list.popleft()[1]
        return self.d.pop(key)

    def min(self):
        return self.d[self.list[0][1]]

    def remove(self, key):
        d = self.d.pop(key)
        self.list.remove((d.f, key))

    def empty(self):
        return not len(self.list)
