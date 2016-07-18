#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os.path
import argparse
from itertools import repeat
import csv

def main():
    x = 0
    parser = argparse.ArgumentParser()
    parser.add_argument('--f', type=str, help='function name', required=True)
    parser.add_argument('--x', type=int, help='integer')
    parser.add_argument('--i', type=str, help='input file')
    args = parser.parse_args()

    func = getattr(sys.modules[__name__], args.f)
    if args.x:
        res = func(args.x)        
        print(res)

    if args.i:
        if os.path.isfile(args.i):
            with open(args.i,'rb') as fp:
                delimiter = ','
                reader = csv.reader(fp)
                for row in reader:
                    res = map(str,func(int(row[0])))
                    print(row[0] + ',' + ','.join(res))

        else:
            print(args.i + ' is not exist.')

    sys.exit(0)

 
def get_divisor_sum(x):
    if x == 0:
        return 0

    f = lambda i,n: i+n if x % n == 0 else i

    return reduce(f,range(1, x + 1))

def prime_factorization(x):
        
    n = 2
    res = []
    p = x
    f = lambda x,n,i:f(x/n,n,i+1) if x % n == 0 else (x,i)

    while n <= x:
        if is_prime(n) != False:
            p,i = f(p,n,0)
            res.extend(list(repeat(n,i)))
            if p == 1:
                break

        n += 1

    return res


def is_prime(x):

    if x < 2:
        return False

    if x == 2:
        return x

    if x % 2 == 0:
        return False

    n = 3
    while n <= x/n:
        if x % n == 0:
            return False
        n += 2

    return x



if __name__ == "__main__":
    main()
