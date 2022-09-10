from key import genKeys, genBit
from oaep import oaepEnc, oaepDec
from aes import aesEnc, aesDec
from utils import power, gridToStr, strToGrid

# Encrypt a message -> message**e % n
def encMessage(message: int, e: int, n: int) -> str:
  eVal = hex(power(message, e, n))[2:]
  return eVal
  
# Decrypt a message -> message**d % n
def decMessage(message: str, d: int, n: int) -> int:
  dVal = power(int(message, 16), d, n)
  return dVal

# Encrypt a message using RSA-OAEP
def rsaEnc(message: bytes, n: int, e: int, aesKey: str, aesIV: str) -> list:

  # Encrypt with AES @TODO ? @HARDCODED
  # Encrypt message (16 byte blocks)
  aesMes = aesEnc(aesKey, plaintext, aesIV)

  # List of AES-OAEP-RSA encrypted blocks
  encMesBlocks = []

  for block in aesMes:
    
    # Encode block with OAEP
    byteBlock = bytearray.fromhex(gridToStr(block))
    em = oaepEnc(byteBlock)

    # Encrypt message with RSA
    encMes = encMessage(int(em.hex(), 16), int(e, 16), int(n, 16))
    encMesBlocks.append(encMes)

  return encMesBlocks

# Decrypt a message encoded with RSA-OAEP
def rsaDec(encMes: list, n: int, d: int, aesKey: str, aesIV: str) -> str:
  
  decMesBlocks = []

  for block in encMes:
    
    # Decrypt RSA cypher
    decMes = decMessage(block, int(d, 16), int(n, 16)).to_bytes(97, "big") # @TODO hardcoded 97 (16 bytes)

    # Decode OAEP message
    m = oaepDec(decMes).hex()
    decMesBlocks.append(strToGrid(m))
  
  # Decrypt AES blocks
  decAesMes = aesDec(aesKey, decMesBlocks, aesIV)

  return decAesMes

# DEBUG
e, d, n = genKeys(1024)
e = hex(e)[2:]
d = hex(d)[2:]
n = hex(n)[2:]

print("\nE:", e)
print("\nD:", d)
print("\nN:", n)

# Plaintext => 128 bits - 16 bytes - 32 digit hexadecimal string
plaintext = "1123456789abcdef0123477789abcdefabcdef0123456789abcdef0123456789aedfaedfaedfaedfaedfaedfaedfaedf"
# aesKey    = "19a09ae93df4c6f8e3e28d48be2b2a08"
# aesIV     = "01928374659987655443102938475621"

# Generate random 128 bit key and IV for AES
aesKey = f"{genBit(128):032x}"
aesIV  = f"{genBit(128):032x}"

print("\nAES KEY:", aesKey)
print("\nAES IV:", aesIV)
print("\nPLAINTEXT:", plaintext)

byteMessage = bytearray.fromhex(plaintext)

rsaEncBlocks = rsaEnc(byteMessage, n, e, aesKey, aesIV)
print("\nRSA ENC:")
for block in rsaEncBlocks: print(block)

rsaDecMes = rsaDec(rsaEncBlocks, n, d, aesKey, aesIV)
print("\nRSA DEC:", rsaDecMes)

assert(rsaDecMes == plaintext)