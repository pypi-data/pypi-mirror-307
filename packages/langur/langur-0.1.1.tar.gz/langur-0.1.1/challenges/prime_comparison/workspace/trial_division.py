def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def find_primes(n):
    return [i for i in range(n + 1) if is_prime(i)]

if __name__ == '__main__':
    import time
    n = 1000000
    start = time.time()
    primes = find_primes(n)
    end = time.time()
    print(f'Trial division method took {end - start:.4f} seconds')
    print(f'Found {len(primes)} prime numbers')