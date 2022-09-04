# Part 2 -> Cypher a message (AES-CTR mode)

from part1 import genKey
from utils import SBOX
from utils import np, textwrap
from utils import strToGrid, gmul, expandKey

# Key and Plaintext -> 128 bit block
def aesEnc(key, plaintext, iv):

  # Initializes the 128 bit counter
  counter = "0" * 32
  blocks = []
  
  # Runs AES for all blocks
  for pText in plaintext:

    state = strToGrid(f"{(int(iv, 16) + int(counter, 16)):032x}")

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

    # This is the step (Mi XOR Ek(IV + counter))
    # the addRoundKey func was used for its convenience
    state = addRoundKey(state, pText)
    blocks.append(state)

    # Increment counter
    counter = f"{(int(counter, 16) + 1):032x}"

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

# Key, Plaintext and IV
key       = "19a09ae93df4c6f8e3e28d48be2b2a08"
plaintext = "1123456789abcdef0123456789abcdefabcdef0123456789abcdef0123456789"
iv        = "01928374659987655443102938475621"

# Hardcoded
key = textwrap.fill(key, 8).split('\n')
plaintext = textwrap.fill(plaintext, 32).split('\n')

# Input
# key = textwrap.fill(input("Enter key (Hexadecimal 32 digits): "), 8).split('\n')
# plaintext = textwrap.fill(input("Enter plaintext (Blocks of 32 Hexadecimal digits): "), 32).split('\n')
# iv = input("Enter IV (Hexadecimal 32 digits): ")

blocks = aesEnc(key, plaintext, iv)

for i in blocks:
  print(i)
