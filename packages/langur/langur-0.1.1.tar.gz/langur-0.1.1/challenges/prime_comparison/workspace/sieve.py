def sieve_of_eratosthenes(n):
    primes = [True] * (n + 1)
    primes[0] = primes[1] = False
    
    for i in range(2, int(n ** 0.5) + 1):
        if primes[i]:
            for j in range(i * i, n + 1, i):
                primes[j] = False
    
    return [i for i in range(n + 1) if primes[i]]

if __name__ == '__main__':
    import time
    n = 1000000
    start = time.time()
    primes = sieve_of_eratosthenes(n)
    end = time.time()
    print(f'Sieve method took {end - start:.4f} seconds')
    print(f'Found {len(primes)} prime numbers')