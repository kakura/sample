#!/usr/bin/python
# -*- coding:utf-8 -*-

# Get divisor.

import sys
import argparse


def main():
    x = 0
    parser = argparse.ArgumentParser()
    parser.add_argument('--x', type=int, help='integer')
    args = parser.parse_args()

    divisor_sum = get_divisor_sum(args.x)

    print(divisor_sum)
    sys.exit(0)


def get_divisor_sum(x):
    if x == 0:
        return 0

    res = 0
    for n in range(1, x + 1):
        res += n if x % n == 0 else 0

    return res

if __name__ == "__main__":
    main()
