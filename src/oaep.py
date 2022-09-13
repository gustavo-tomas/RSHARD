# https://en.wikipedia.org/wiki/Optimal_asymmetric_encryption_padding#Encoding
# https://en.wikipedia.org/wiki/Mask_generation_function#Padding_schemes

from key import genBit
from sha3 import sha3_256
import hashlib

# Masking function
def mgf1(seed: bytes, length: int, hash_func=hashlib.sha3_256) -> bytes:
  hLen = hash_func().digest_size
  assert(length < (hLen << 32))

  T = b""
  counter = 0
  while len(T) < length:
    C = int.to_bytes(counter, 4, 'big')
    T += hash_func(seed + C).digest()
    counter += 1
  return T[:length]

# OAEP encoding function
def oaepEnc(m: bytes) -> [bytes, bytes]:

  lHash = sha3_256(bytearray("", "utf-8"))                    # Hash label (label is "")

  mLen = len(m)                                               # Message length in bytes
  hLen = len(lHash)                                           # Hash length in bytes
  k = 3 * hLen + 1                                            # RSA % n in bytes (2 * hLen + 1 ?)
  psLen = k - mLen - 2 * hLen - 2                             # PS length
  ps = bytearray([0x00 for i in range(psLen)])                # Generate a padding string

  db = lHash + ps + b'\x01' + m                               # Concatenate lHash || PS || 0x01 || M
  assert(len(db) == k - hLen - 1)
  seed = genBit(hLen * 8).to_bytes(hLen, "big")               # Generate a seed with length hLen
  dbMask = mgf1(seed, k - hLen - 1)                           # Generate a mask for the db
  maskedDB = bytes(a ^ b for (a, b) in zip(db, dbMask))       # Mask the data block with the mask
  seedMask = mgf1(maskedDB, hLen)                             # Generate a mask for the seed
  maskedSeed = bytes(a ^ b for (a, b) in zip(seed, seedMask)) # Mask the seed with the generated mask
  em = b'\x00' + maskedSeed + maskedDB                        # Make padded message
  
  return em, lHash

# OAEP decoding function (inverse of oaepEnc)
def oaepDec(em: bytes, lHash: bytes) -> bytes:

  hLen = len(lHash)
  k = 3 * hLen + 1
  emWithoutZero = em.split(b'\x00', 1)[1]
  maskedSeed = emWithoutZero[0:hLen]
  maskedDB = emWithoutZero[hLen:]
  seedMask = mgf1(maskedDB, hLen)
  seed = bytes(a ^ b for (a, b) in zip(maskedSeed, seedMask))
  dbMask = mgf1(seed, k - hLen - 1)
  db = bytes(a ^ b for (a, b) in zip(maskedDB, dbMask))
  lHash2 = db[:len(lHash)]
  assert(lHash == lHash2)
  db = db.split(lHash, 1)[1]
  db = db.split(b'\x01', 1)[1]
  m = db

  return m
