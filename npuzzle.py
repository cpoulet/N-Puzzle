#!/usr/bin/env python3

###############################################################################
#            _   _        _____  _    _ _____________      ______             #
#           | \ | |      |  __ \| |  | |___  /___  / |    |  ____|            #
#           |  \| |______| |__) | |  | |  / /   / /| |    | |__               #
#           | . ` |______|  ___/| |  | | / /   / / | |    |  __|              #
#           | |\  |      | |    | |__| |/ /__ / /__| |____| |____             #
#           |_| \_|      |_|     \____//_____/_____|______|______|            #
#                                                                             #
###############################################################################

import sys

from nsolver import NSolver
import utils

def main(argv):
    if len(argv) > 2:
        print("usage: ./npuzzle [input_path]\n\nif no input_path are given, a random solvable grid will be generated with a size of users choice")
        return
    NS = NSolver()
    if len(argv) == 2:
        NS.parse(argv[1].strip())
    else:
        NS.generate()
    NS.solve()

if __name__ == "__main__":
    try:
        main(sys.argv)
    except Exception as e:
        if str(e):
            print('Error : ' + str(e))
