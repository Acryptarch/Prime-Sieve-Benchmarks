# Prime Sieve Benchmarker
The purpose of this project is to benchmark and time variations of the Sieve of Erasthoneses. It uses many methods including but not limited to list slicing, vectorization, and a speed up array operations with the use of numpy

## Requirements
- Python 3.6+
- numpy: Can be downloaded with `pip install numpy`

## Getting Started

```python
import prime_eratosthenes as pe

pe.prime_sieve2c(limit=20) #Returns prime numbers up to 20
'''[2, 3, 5, 7, 11, 13, 17, 19]'''

#Process to benchmark the speed of each method
pe.test_val = 100
pe.benchmark(pe.prime_methods, repeat=10) #Times each method repeat times and returns the average for each

'''
Benchmark with input of 100
npprime_sieve3c: 3.24 ms
npprime_sieve1c: 8.91 ms
prime_sieve2c: 63.37 ms
prime_sieve3b: 68.27 ms
'''
```
