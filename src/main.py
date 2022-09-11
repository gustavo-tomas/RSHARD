from key import genKeys, genBit
from rsa import rsaEnc, rsaDec

def main():
  
  # Plaintext => 128 bits - 16 bytes - 32 digit hexadecimal string
  plaintext = "1123456789abcdef0123477789abcdefabcdef0123456789abcdef0123456789aedfaedfaedfaedfaedfaedfaedfaedf"
  plaintext = input("Enter a plaintext: ")
  
  # Padding plaintext with 0
  mesLen = 32
  if len(plaintext) > 32:
    mesLen += 32 * (len(plaintext) // 32)

  plaintext += "0" * (mesLen - len(plaintext))
  print("PADDED PLAINTEXT:", plaintext)

  # Generate RSA parameters
  e, d, n = genKeys(1024)
  e = hex(e)[2:]
  d = hex(d)[2:]
  n = hex(n)[2:]

  print("\nE:", e)
  print("\nD:", d)
  print("\nN:", n)

  # Generate random 128 bit key and IV for AES
  aesKey = f"{genBit(128):032x}"
  aesIV  = f"{genBit(128):032x}"

  print("\nAES KEY:", aesKey)
  print("\nAES IV:", aesIV)
  print("\nPLAINTEXT:", plaintext)

  rsaEncBlocks = rsaEnc(plaintext, n, e, aesKey, aesIV)
  print("\nRSA ENC:")
  for block in rsaEncBlocks: print(block)

  rsaDecMes = rsaDec(rsaEncBlocks, n, d, aesKey, aesIV)
  print("\nRSA DEC:", rsaDecMes)

  assert(rsaDecMes == plaintext)
  return

if __name__ == "__main__":
  main()
