#!/usr/bin/env python

import sys
import math
import itertools


"""
Python play
"""


# This is a generator because it is a function with a "yield" in it.
def fibs(count=None):
    if count is not None and count < 1:
        return
    a = 1
    b = 1
    yield a
    if count is not None and count < 2:
        return
    yield b
    if count is None:
        while 1:
            c = a + b
            yield c
            a = b
            b = c
    while count > 2:
        c = a + b
        yield c
        a = b
        b = c
        count -= 1

# This is a also generator
def approx_fibs(count=None):
    s = math.sqrt(5)
    r = (1 + s)/2  # golden ratio
    x = 1

    if count is None:
        my_iterator = itertools.count(start=0, step=1)
    else:
        my_iterator = range(count)

    for i in my_iterator:
        x *= r
        yield x/s

def fibbonicci_demo(n):
    for i, f, x in zip(range(1, n+1), fibs(n), approx_fibs(n)):
        print(" %2d : %4d - %6.3f = %7.3f " % (i, f, x, f-x))

def doubler(gen):
    for x in gen:
        yield x*2

def limiter(gen, n=None):
    count = -1 if n is None else n
    for x in gen:
        if not count:
            return
        yield x
        count -= 1

def primes():
    # All the primes ...
    primes = [2]  # seeding the prime number database
    yield 2  # The only even prime.
    p = 3
    while True:
        q = int(math.sqrt(p))  # max prime needed for testing
        for i in primes:
            if i > q:
                primes.append(p)
                yield p  # i is not a factor of p, for all i < q
                break
            r = p / i
            if r == int(r):
                break
        p += 2  # select next prime candidate


if __name__ == "__main__":

    if sys.version_info.major != 3:
        sys.stderr.write("Only Python 3 is supported.\n")
        sys.exit(1)

    print("Finonacci numbers with Binet's formula")
    fibbonicci_demo(15)
    print()

    # A sampler of four numbers from the generator
    print("Just four Finonacci numbers")
    generator = fibs(4)
    for i in range(4):
        print(generator.__next__(), end=" ")
    print()

    # Show how to stop, continue, and stop an infinite generator
    print("more fun with generators")
    generator = fibs()
    for i in range(2):
        print(generator.__next__())
    for x in generator:
        print(x, end=" ")
        if x > 8:
            break
    print()  # finish the line
    print()
    print("Chaining generators")
    print(list(doubler(fibs(8))))

    print()
    print("Some Primes")
    print(list(limiter(primes(), 25)))
