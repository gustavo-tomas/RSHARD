# Part 2 -> Cypher a message (AES-CTR mode)

from part1 import genKey
from utils import SBOX
from utils import np, textwrap
from utils import hexXor, strToGrid, gmul, expandKey, formatPlaintext, formatKey

# Key and Plaintext -> 128 bit block
def aesEnc(key, plaintext):

  # Convert key to a 128 bit hex
  key = ['19a09ae9', '3df4c6f8', 'e3e28d48', 'be2b2a08']

  # Run AES for all states (blocks)
  states = [strToGrid("0123456789abcdef0123456789abcdef"), strToGrid("abcdef0123456789abcdef0123456789")]
  blocks = []
  
  for state in states:

    # Key expansion
    expandedKey = textwrap.fill(''.join(expandKey(key, 11)), 32).split('\n')
    keyCounter = 0

    # Initial round
    state = addRoundKey(state, expandedKey[keyCounter])
    keyCounter += 1

    # Main rounds
    for r in range(0, 9):
      state = subBytes(state)
      state = shiftRows(state)
      state = mixColumns(state)
      state = addRoundKey(state, expandedKey[keyCounter])
      keyCounter += 1

    # Final round
    state = subBytes(state)
    state = shiftRows(state)
    state = addRoundKey(state, expandedKey[keyCounter])

    blocks.append(state)
  
  return blocks

def subBytes(state):
  for row in range(0, 4):
    for col in range(0, 4):
      newState = SBOX[int(state[row][col][0], 16)][int(state[row][col][1], 16)]
      state[row][col] = newState
 
  return state

def shiftRows(state):
  for row in range(4):
    column = []
    for col in range(4):
      column.append(state[col][row])

    column = np.roll(column, -row).tolist()
    for col in range(4):
      state[col][row] = column[col]
    
  return state

def mixColumns(state):
  newState = [[0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0]]

  column = [0, 0, 0, 0]

  for i in range(4):
    for j in range(4):
      column[j] = int(state[i][j], 16)

    newState[i][0] = f"{gmul(column[0], 2) ^ gmul(column[1], 3) ^ gmul(column[2], 1) ^ gmul(column[3], 1):02x}"
    newState[i][1] = f"{gmul(column[0], 1) ^ gmul(column[1], 2) ^ gmul(column[2], 3) ^ gmul(column[3], 1):02x}"
    newState[i][2] = f"{gmul(column[0], 1) ^ gmul(column[1], 1) ^ gmul(column[2], 2) ^ gmul(column[3], 3):02x}"
    newState[i][3] = f"{gmul(column[0], 3) ^ gmul(column[1], 1) ^ gmul(column[2], 1) ^ gmul(column[3], 2):02x}"

  state = newState

  return state

def addRoundKey(state, key):
  gridKey = strToGrid(key)
  for i in range(4):
    for j in range(4):
      state[i][j] = f"{int(state[i][j], 16) ^ int(gridKey[i][j], 16):02x}"
      
  return state

# key = ["0f1571c9", "47d9e859", "0cb7add6", "af7f6798"]
key = "aaaaaaaaaaaaaaaa"
plaintext = "abcdefghabcdefgh"
blocks = aesEnc(key, plaintext)

for i in blocks:
  print(i)
