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

import os
import argparse

import utils
from nsolver import NSolver

def main():
    parser = argparse.ArgumentParser(description='Solver of Taquin\nIf no grid are given as input, a random solvable grid will be generated with a size of users choice')
    parser.add_argument('input', nargs='?', default=False, help='Input file describing the taquin grid.')
    parser.add_argument('-q', '--quiet', action='store_true', help='quiet mode')
    parser.add_argument('-g', '--greedy', action='store_true', help='greedy mode')
    parser.add_argument('-u', '--uniformcost', action='store_true', help='uniform cost mode')
    parser.add_argument('-v', '--visual', action='store_true', help='visual mode')
    args = parser.parse_args()
    NS = NSolver(args.quiet, args.greedy, args.uniformcost, args.visual)
    if args.input:
        if not os.path.exists(args.input) or not os.path.isfile(args.input):
            raise Exception('File not found: "' + args.input + '".')
        NS.parse(args.input)
    else:
        NS.generate()
    NS.solve()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if str(e):
            print('Error : ' + str(e))
