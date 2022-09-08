from key import genKeys
from oaep import oaepEnc, oaepDec
from utils import power

# Encrypt a message -> message**e % n
def encMessage(message: int, e: int, n: int) -> str:
  eVal = hex(power(message, e, n))[2:]
  return eVal
  
# Decrypt a message -> message**d % n
def decMessage(message: str, d: int, n: int) -> int:
  dVal = power(int(message, 16), d, n)
  return dVal

# Encrypt a message using RSA-OAEP
def rsaEnc(message: bytes, n: int, e: int) -> str:

  # Encode message with OAEP
  em = oaepEnc(message)

  # Encrypt message with RSA
  encMes = encMessage(int(em.hex(), 16), int(e, 16), int(n, 16))

  return encMes

# Decrypt a message encoded with RSA-OAEP
def rsaDec(encMes: str, n:int, d: int) -> bytes:
  
  # Decrypt RSA cypher
  decMes = decMessage(encMes, int(d, 16), int(n, 16)).to_bytes(97, "big") # @TODO hardcoded 97 (16 bytes)

  # Decode OAEP message
  m = oaepDec(decMes)

  return m

message = bytearray([0x03 for i in range(16)]) # 16 bytes - increase "k" for larger size
print("MESSAGE:", message.hex())

e, d, n = genKeys(1024)
e = hex(e)[2:]
d = hex(d)[2:]
n = hex(n)[2:]

print("E:", e, "\nLEN:", len(e))
print("D:", d, "\nLEN:", len(d))
print("N:", n, "\nLEN:", len(n))

rsaE = rsaEnc(message, n, e)
print("RSA ENC:", rsaE)

rsaD = rsaDec(rsaE, n, d)
print("RSA DEC:", rsaD.hex())

assert(rsaD == message)