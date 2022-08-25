# Part 1 -> Generate a 1024 bit prime

import random, math

# Generate a random number between 2^(n-1) + 1 and 2^(n) - 1 -> avoid small primes
def genBit(n):
	return random.randrange(2**(n-1) + 1, 2**(n) - 1)

# List of the first few primes
primesList = []

# Generates first few primes using the sieve of eratosthenes
def genPrimesList(n):
  prime = [True for i in range(n + 1)]
  p = 2
  
  while p * p <= n:
    if prime[p] == True:
      for i in range(p * p, n + 1, p): prime[i] = False
    p += 1
  
  for p in range(2, n+1):
    if prime[p]: primesList.append(p)

# Tests if generated number of n bits is prime
def getLowLevelPrime(n):
  while True:
    primeCandidate = genBit(n)
    for divisor in primesList:
      if primeCandidate % divisor == 0 and divisor**2 <= primeCandidate:
        break
      else: 
        return primeCandidate

# Run the Miller-Rabin test n times
def passesMillerRabin(possiblePrime, n):

	maxDivisionsByTwo = 0
	evenComponent = possiblePrime-1

	while evenComponent % 2 == 0:
		evenComponent >>= 1
		maxDivisionsByTwo += 1
	assert(2**maxDivisionsByTwo * evenComponent == possiblePrime-1)

	def trialComposite(roundTester):
		if pow(roundTester, evenComponent, possiblePrime) == 1:
			return False
		for i in range(maxDivisionsByTwo):
			if pow(roundTester, 2**i * evenComponent, possiblePrime) == possiblePrime - 1:
				return False
		return True

	for i in range(n + 1):
		roundTester = random.randrange(2, possiblePrime)
		if trialComposite(roundTester):
			return False
	return True


def main():
  # Generates the first few primes
  genPrimesList(500)

  # Generates a Miller-Rabin approved prime
  while True:
    number = getLowLevelPrime(1024)   # Gets possible prime
    if passesMillerRabin(number, 20): # Runs the MR test with n rounds
      print("MR:", number)
      break

  # FOR TEST PURPOSES ONLY
  from Crypto.Util import number
  testPrime = number.getPrime(1024)
  print("TEST:", testPrime)

if __name__ == "__main__": main()

