from key import genKeys
from rsa import rsaEnc, rsaDec

def main():
  
  # Plaintext => 128 bits - 16 bytes - 32 digit hexadecimal string
  plaintext = input("ENTER PLAINTEXT (HEX): ")
  
  # Padding plaintext with 0
  mesLen = 32
  if len(plaintext) > 32:
    mesLen += 32 * (len(plaintext) // 32)

  plaintext += "0" * (mesLen - len(plaintext))
  print("\nPADDED PLAINTEXT:", plaintext)

  # Generate RSA parameters
  e, d, n = genKeys(1024)
  e = hex(e)[2:]
  d = hex(d)[2:]
  n = hex(n)[2:]

  print("\nE:", e)
  print("\nD:", d)
  print("\nN:", n)

  aesEncBlocks, rsaEncHash, rsaEncKey, aesIV = rsaEnc(plaintext, n, e)
  message = rsaDec(aesEncBlocks, n, d, rsaEncHash, rsaEncKey, aesIV)

  assert(message == plaintext)
  return

if __name__ == "__main__":
  main()
