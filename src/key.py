from utils import random, math

# Generate a random number between 2^(n-1) + 1 and 2^(n) - 1 -> avoid small primes
def genBit(n: int) -> int:
  return random.randrange(2**(n-1) + 1, 2**(n) - 1)

# List of the first few primes
primesList = []

# Generates first few primes using the sieve of eratosthenes
def genPrimesList(n: int) -> None:
  prime = [True for i in range(n + 1)]
  p = 2

  while p * p <= n:
    if prime[p] == True:
      for i in range(p * p, n + 1, p):
        prime[i] = False
    p += 1

  for p in range(2, n+1):
    if prime[p]:
      primesList.append(p)

# Tests if generated number of n bits is prime
def getPossiblePrime(n: int) -> int:
  while True:
    primeCandidate = genBit(n)
    for divisor in primesList:
      if primeCandidate % divisor == 0 and divisor**2 <= primeCandidate:
        break
      else:
        return primeCandidate

# Runs the Miller-Rabin test n times
def passesMillerRabin(possiblePrime: int, n: int) -> bool:

  maxDivisionsByTwo = 0
  evenComponent = possiblePrime-1

  while evenComponent % 2 == 0:
    evenComponent >>= 1
    maxDivisionsByTwo += 1
  assert (2**maxDivisionsByTwo * evenComponent == possiblePrime-1)

  # Checks if number is a composite
  def trialComposite(roundTester: int) -> bool:
    if pow(roundTester, evenComponent, possiblePrime) == 1:
      return False
    for i in range(maxDivisionsByTwo):
      if pow(roundTester, 2**i * evenComponent, possiblePrime) == possiblePrime - 1:
        return False
    return True

  # Amount of times to run the test
  for i in range(n):
    roundTester = random.randrange(2, possiblePrime)
    if trialComposite(roundTester):
      return False
  return True

# Generates a prime number
def genPrime(n: int) -> int:

  # Generates the first few primes
  genPrimesList(500)

  # Generates a Miller-Rabin approved prime
  primeNum = ""
  while True:
    possiblePrime = getPossiblePrime(n)   # Gets possible prime
    if passesMillerRabin(possiblePrime, 20):  # Runs the MR test with n rounds
      primeNum = possiblePrime
      break
  
  return primeNum

# Generates public and private key with size n
def genKeys(n: int) -> [int, int, int]:

  p = genPrime(n)         # p prime
  q = genPrime(n)         # q prime
  n = p * q               # n
  t = (p - 1) * (q - 1)   # t (Euler Totient)

  # Choose e
  for e in range(t - 1, 1, -1):
    if math.gcd(e, t) == 1 and math.gcd(e, n) == 1:
      break

  # Choose d
  d = (t * (t - 1) - 1)

  assert((e * d) % t == 1)
  return e, d, n
