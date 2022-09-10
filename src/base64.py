# https://en.wikibooks.org/wiki/Algorithm_Implementation/Miscellaneous/Base64
from utils import re
from utils import zfrs

base64Chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

# Encode string to base64
def base64Enc(s: str) -> str:
  
  r = ""
  p = ""
  c = len(s) % 3

  # Padding with zero to make s a multiple of 3
  if c > 0 and c < 3:
    p += "=" * (3 - c)
    s += "\0" * (3 - c)

  for c in range(0, len(s), 3):
    
    # Newline after 76 characters
    if c > 0 and (c / 3 * 4) % 76 == 0:
      r += "\r\n"

    n = (ord(s[c]) << 16) + (ord(s[c + 1]) << 8) + ord(s[c + 2])
    n = [zfrs(n, 18) & 63, zfrs(n, 12) & 63, zfrs(n, 6) & 63, n & 63]
    
    for i in range(4):
      r += base64Chars[n[i]]

  # Add the padding after removing the zero padding
  return r[0:len(r)-len(p)] + p

# Decode base64 to string
def base64Dec(s: str) -> str:

  s = re.sub(r'[^' + base64Chars + r'=]', '', s)
  p = ""
  r = ""

  # Replace padding with a zero
  if s[-1] == "=":
    if s[-2] == "=":
      p = 'AA'
    else:
      p = 'A'
  else:
    p = ''

  s = s[0:len(s)-len(p)] + p

  for c in range(0, len(s), 4):
    n = (base64Chars.index(s[c]) << 18) + (base64Chars.index(s[c+1]) << 12)
    n += (base64Chars.index(s[c+2]) << 6) + base64Chars.index(s[c+3])

    r += chr(zfrs(n, 16) & 255)
    r += chr(zfrs(n, 8) & 255)
    r += chr(n & 255)

  return r[0:len(r)-len(p)]

# DEBUG
# b64encoded = base64Enc("boiboiboiboidacarapretapegaessemeninhoquetemmedodecareta")
# print("B64", b64encoded)

# b64decoded = base64Dec(b64encoded)
# print("DEC", b64decoded)