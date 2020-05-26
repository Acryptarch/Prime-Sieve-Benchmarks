import math
import timeit
import numpy as np

def convert(bool_list):
    """Helper method that converts a boolean list of prime numbers (index is value and bool value determines
    primality) into an integer list that is easier to process"""
    return [i for i in range(2, len(bool_list)) if bool_list[i]]


test_val = 10 ** 6 # Modify this variable to change the values inputted in the benchmark method.


def benchmark(method_list, repeat=1):
    """Given a list of methods that return a list of prime numbers up to a given number, the method prints out the
    time for each method to run and ranks them. The time is measured by using the timeit function from the time it
    module. The repeat variable controls how precise the average run time is. Increasing it will run each function
    multiple times which results in a more precise average. The value inputted into each method can be modified by
    changing test_val"""
    print("Benchmark with input of " + str(test_val))
    collection = {}

    for val in method_list:
        collection[val.__name__] = round((((timeit.timeit(stmt=val, number=repeat)) / repeat) * 1000), 2) #average->ms

    sorted_times = [(k, collection[k]) for k in sorted(collection, key=collection.get, reverse=False)]

    for name, value in sorted_times:
        print(f'{name}: {value} ms')


def generate_txt(method, value, filename='prime'):
    """Generates a text file of primes from a list of primes from method(value)"""
    primes = method(value)
    max_length = math.ceil(math.log10(value)) + 3
    append_state = "{0:<" + str(max_length) + "}"
    print("calculations complete")
    with open(filename, 'w') as f:
        text = ''
        for i in range(0, len(primes)):
            if i % 10 == 0 and i != 0:
                text += '\n'

            text += append_state.format(primes[i])

        f.write(text)


def txt_tolist(file):
    """Converts a text file of prime numbers to a list of prime numbers"""
    with open(file, 'r') as f:
        f_contents = f.read()
        prime_string = f_contents.split()
        primes = [int(i) for i in prime_string]
        return primes


def prime_sieve1a(limit=test_val):
    """A prime sieve that checks until the square root of the limit. It is an ancient algorithm that works by
    marking the multiples of each prime found, which leaves the prime numbers in the array unmarked in the end"""
    prime = [True] * (limit + 1)
    prime[0] = prime[1] = False
    max_lim = int(limit ** 0.5) + 1
    for i in range(0, max_lim):
        if prime[i]:
            for n in range(i * i, limit + 1, i):
                prime[n] = False

    return convert(prime)


def prime_sieve1b(limit=test_val):
    """A sieve that is optimized through the vectorization of the for loop that eliminates multiples"""
    prime = [True] * (limit + 1)
    prime[0] = prime[1] = False
    max_lim = int(limit ** 0.5) + 1
    for i in range(0, max_lim):
        if prime[i]:
            prime[i * i::i] = [False] * (((limit - (i * i)) // i) + 1)

    return convert(prime)


def npprime_sieve1c(limit=test_val):
    """A sieve that is optimized by using the numpy library"""
    prime = np.ones(limit + 1, dtype=np.bool)
    prime[0] = prime[1] = False
    max_lim = int(limit ** 0.5) + 1
    for i in range(0, max_lim):
        if prime[i]:
            prime[i * i::i] = False

    return np.nonzero(prime)


def prime_sieve2a(limit=test_val):
    """A sieve that creates an array which automatically marks even numbers as False. The even numbers are
    not checked in vectorized version of the inner for loop because the increment is twice the prime number"""
    prime = [False, False, True] + [True, False] * (((limit - 2) // 2) + 1)
    del prime[limit + 1:]
    max_lim = int(limit ** 0.5) + 1
    for x in range(3, max_lim, 2):
        if prime[x]:
            for i in range(x * x, limit + 1, 2 * x):
                prime[i] = False

    return convert(prime)


def prime_sieve2b(limit=test_val):
    """A sieve that ignores even numbers by iterating over it in the inner for loop and the final
    process to convert the boolean list to an integer list of prime numbers"""
    prime = [True] * (limit + 1)
    prime[0] = prime[1] = False
    max_lim = int(limit ** 0.5) + 1
    for i in range(3, max_lim, 2):
        if prime[i]:
            for n in range(i ** 2, limit + 1, i * 2):
                prime[n] = False
    return [2] + [x for x in range(3, limit + 1, 2) if prime[x]]


def prime_sieve2c(limit=test_val):
    """A sieve that ignores even numbers by iterating over it in vectorized list assignment and the final
    process to convert the boolean list to an integer list of prime numbers"""
    prime = [True] * (limit + 1)
    prime[0] = prime[1] = False
    max_lim = int(limit ** 0.5) + 1
    for i in range(3, max_lim, 2):
        if prime[i]:
            prime[i ** 2::2 * i] = [False] * (((limit - i ** 2) // (2 * i)) + 1)
    return [2] + [x for x in range(3, limit + 1, 2) if prime[x]]


def npprime_sieve2d(limit=test_val):
    """A sieve that ignores even numbers by iterating over it in vectorized list assignment and the final
    process to convert the boolean list to an integer list of prime numbers. Numpy is used for optimization"""
    prime = np.ones(limit + 1, dtype=np.bool)
    prime[0] = prime[1] = False
    max_lim = int(limit ** 0.5) + 1
    for i in range(3, max_lim, 2):
        if prime[i]:
            prime[i ** 2::2 * i] = False
    return [2] + [x for x in range(3, limit + 1, 2) if prime[x]]


def prime_sieve2e(limit=test_val):
    """A sieve that is identical to method 2c except that the conversion from bool list to integer list
    skips multiples of 2 and 3"""
    prime = [True] * (limit + 1)
    prime[0] = prime[1] = False
    max_lim = int(limit ** 0.5) + 1
    for i in range(3, max_lim, 2):
        if prime[i]:
            prime[i ** 2::2 * i] = [False] * (((limit - i ** 2) // (2 * i)) + 1)

    prime_num = [2, 3]
    num = 5
    increment = 2
    while num <= limit:
        if prime[num]:
            prime_num.append(num)
        num += 2
        increment = 6 - increment
    return prime_num


def prime_sieve3a(limit=test_val):
    """"A sieve that creates an array half the size of the number set being analyzed to iterate over
    the even numbers. The array is interpreted as a set of odd numbers and the math has been adapted as such"""
    limit += 1
    prime = [True] * (limit // 2)
    max_lim = int(limit ** 0.5) + 1
    for i in range(3, max_lim, 2):
        if prime[i // 2]:
            for x in range(i * i // 2, limit // 2, i):
                prime[x] = False
    return [2] + [2 * x + 1 for x in range(1, limit // 2) if prime[x]]


def prime_sieve3b(limit=test_val):
    """"A sieve that creates an array half the size of the number set being analyzed to iterate over
    the even numbers. The array is interpreted as a set of odd numbers and the math has been adapted as such. The
    previous inner for loop has been vectorized for optimization"""

    limit += 1
    prime = [True] * (limit // 2)
    max_lim = int(limit ** 0.5) + 1
    for i in range(3, max_lim, 2):
        if prime[i // 2]:
            prime[i * i // 2::i] = [False] * ((limit - i * i - 1) // (2 * i) + 1)

    return [2] + [2 * x + 1 for x in range(1, limit // 2) if prime[x]]


def npprime_sieve3c(limit=test_val):
    """A sieve similar to version 3b which is further optimized by the numpy library"""
    limit += 1
    prime = np.ones(limit // 2, dtype=np.bool)
    max_lim = int(limit ** 0.5) + 1
    for i in range(3, max_lim, 2):
        if prime[i // 2]:
            prime[i * i // 2::i] = False

    return 2 * np.nonzero(prime)[0][1::] + 1


def main():
    # Methods in this list are called and automatically benchmarked. The value being tested can be modified by
    # changing the test_val variable above the benchmark definition. Increasing the repeat variable will return a
    # more precise average but will take longer to run. Test your own methods by adding them to the prime_methods
    # list below. Make sure the method's default value is set to test_value.

    prime_methods = [prime_sieve1a, prime_sieve1b, npprime_sieve1c, prime_sieve2a, prime_sieve2b,
                     prime_sieve2c, npprime_sieve2d, prime_sieve2e, prime_sieve3a, prime_sieve3b, npprime_sieve3c]

    benchmark(method_list=prime_methods, repeat=1)



if __name__ == '__main__':
    main()
