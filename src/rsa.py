from key import genKeys, genBit
from oaep import oaepEnc, oaepDec
from aes import aesEnc, aesDec
from base64 import base64Enc, base64Dec
from utils import power, gridToStr, strToGrid

# Encrypt a message -> message**e % n
def encMessage(message: int, e: int, n: int) -> str:
  eVal = hex(power(message, e, n))[2:]
  return eVal
  
# Decrypt a message -> message**d % n
def decMessage(message: str, d: int, n: int) -> int:
  dVal = power(int(message, 16), d, n)
  return dVal

# Encrypt a message using AES (and the hash function, aes key with RSA)
def rsaEnc(message: str, n: str, e: str) -> [list, str, str, str]:

  # Generate random 128 bit key and IV for AES
  aesKey = f"{genBit(128):032x}"
  aesIV  = f"{genBit(128):032x}"

  # Encrypt message with AES
  aesEncMes = aesEnc(aesKey, message, aesIV)
  
  # Encode aes key with OAEP
  oaepEncAesKey, lHash = oaepEnc(bytearray().fromhex(aesKey))

  # Encrypt hash and aes key with RSA
  rsaEncHash = encMessage(int(lHash.hex(), 16), int(e, 16), int(n, 16))
  rsaEncKey  = encMessage(int(oaepEncAesKey.hex(), 16), int(e, 16), int(n, 16))

  print("\nHASH:", lHash.hex())
  print("\nAES KEY:", aesKey)
  print("\nAES IV:", aesIV)
  print("\nAES KEY PADDED WITH OAEP AND ENCRYPTED WITH RSA:", rsaEncKey)
  print("\nHASH ENCRYPTED WITH RSA:", rsaEncHash)
  print("\nMESSAGE ENCRYPTED WITH AES:")

  # List of BASE64 encoded blocks
  encMesBlocks = []

  # Encode result in BASE64
  for block in aesEncMes:
    encMes = base64Enc(gridToStr(block))
    encMesBlocks.append(encMes)
    print(encMes)

  return encMesBlocks, rsaEncHash, rsaEncKey, aesIV

# Decrypt a message encoded with AES (and decrypt the previous encoded/encrypted values)
def rsaDec(encMes: list, n: str, d: str, rsaEncHash: str, rsaEncKey: str, aesIV: str) -> str:
  
  # Decrypt hash and aes key
  lHash = decMessage(rsaEncHash, int(d, 16), int(n, 16)).to_bytes(32, "big")
  decAesKey = decMessage(rsaEncKey, int(d, 16), int(n, 16)).to_bytes(97, "big")

  # Decode aes key
  aesKey = oaepDec(decAesKey, lHash).hex()

  # List of decoded BASE64 blocks
  decMesBlocks = []

  # Decode BASE64 blocks
  for block in encMes:
    decBlock = base64Dec(block)
    decMesBlocks.append(strToGrid(decBlock))
  
  # Decrypt AES blocks
  decAesMes = aesDec(aesKey, decMesBlocks, aesIV)

  print("\nDECRYPTED HASH:", lHash.hex())
  print("\nDECRYPTED AES KEY:", aesKey)
  print("\nDECRYPTED AES BLOCKS:", decAesMes)

  return decAesMes
