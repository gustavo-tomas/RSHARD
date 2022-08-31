# Part 2 -> Cypher a message (AES-CTR mode)

from part1 import genKey
from utils import np, SBOX, MIXMAT

state = [['19', 'a0', '9a', 'e9'],
         ['3d', 'f4', 'c6', 'f8'],
         ['e3', 'e2', '8d', '48'],
         ['be', '2b', '2a', '08']]

# Key and Plaintext -> 128 bit block
def aesEnc(key, plaintext):
  # key = hex(genKey(128))

  print(hex(key))
  subBytes(state) # for testing
  shiftRows(state)
  mixColumns(state)
#   # Initial round
#   addRoundKey()

#   # Main rounds
#   for round in range(0, 9):
    # subBytes()
    # shiftRows()
#     mixColumns()
#     addRoundKey()

#   # Final round
#   subBytes()
#   shiftRows()
#   addRoundKey()

  return

# KeyExpansion – round keys are derived from the cipher key using the AES key schedule. AES requires a separate 128-bit round key block for each round plus one more.
# Initial round key addition:

# AddRoundKey – each byte of the state is combined with a byte of the round key using bitwise xor.

# 9, 11 or 13 rounds:
# SubBytes – a non-linear substitution step where each byte is replaced with another according to a lookup table.
# ShiftRows – a transposition step where the last three rows of the state are shifted cyclically a certain number of steps.
# MixColumns – a linear mixing operation which operates on the columns of the state, combining the four bytes in each column.
# AddRoundKey
def subBytes(state):
  for row in range(0, 4):
    for col in range(0, 4):
      newState = SBOX[int(state[row][col][0], 16)][int(state[row][col][1], 16)]
      state[row][col] = newState
 
  return

def shiftRows(state):
  for row in range(4):
    state[row] = np.roll(state[row], -row).tolist()

  return

def mixColumns(state):
  print("STATE:", state)

  column = []
  for c in range(4):
    column.append(state[0][c])

  result = [[0,0,0,0],
          [0,0,0,0],
          [0,0,0,0]]

  # iterate through rows of X
  for i in range(4):
    # iterate through columns of Y
    for j in range(4):
      # iterate through rows of Y
      for k in range(4):
        result[i][j] += MIXMAT[i][k] * int(state[k][j], 16)
        
        for h in range(4):
          print("RES:", result[h])
  
 
  return

def addRoundKey():
  return

# Final round (making 10, 12 or 14 rounds in total):
# SubBytes
# ShiftRows
# AddRoundKey

aesEnc(genKey(128), 'lol')
