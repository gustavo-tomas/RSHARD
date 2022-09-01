# Part 2 -> Cypher a message (AES-CTR mode)

from part1 import genKey
from utils import SBOX, MIXMAT
from utils import np, textwrap
from utils import mult2, mult3, gmul, expand_key

state = [['19', 'a0', '9a', 'e9'],
         ['3d', 'f4', 'c6', 'f8'],
         ['e3', 'e2', '8d', '48'],
         ['be', '2b', '2a', '08']]

# Key and Plaintext -> 128 bit block
def aesEnc(key, plaintext):

  mixColumns(state) # testing

  # # Initial round
  # addRoundKey(state, key)

  # # Main rounds
  # for round in range(0, 9):
  #   subBytes(state)
  #   shiftRows(state)
  #   mixColumns(state)
  #   addRoundKey(state, key)

  # # Final round
  # subBytes(state)
  # shiftRows(state)
  # addRoundKey(state, key)

  return

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
  newState = [[0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0]]

  column = [0, 0, 0, 0]

  for i in range(4):
    for j in range(4):
      column[j] = int(state[i][j], 16)

    newState[i][0] = hex(gmul(column[0], 2) ^ gmul(column[1], 3) ^ gmul(column[2], 1) ^ gmul(column[3], 1))[2:]
    newState[i][1] = hex(gmul(column[0], 1) ^ gmul(column[1], 2) ^ gmul(column[2], 3) ^ gmul(column[3], 1))[2:]
    newState[i][2] = hex(gmul(column[0], 1) ^ gmul(column[1], 1) ^ gmul(column[2], 2) ^ gmul(column[3], 3))[2:]
    newState[i][3] = hex(gmul(column[0], 3) ^ gmul(column[1], 1) ^ gmul(column[2], 1) ^ gmul(column[3], 2))[2:]
  
  state = newState
  print("STATE", state)

  return

def addRoundKey(state, key):
  for i in range(4):
    for j in range(4):
      state[i][j] = hex(int(state[i][j], 16) ^ int(key[i][j], 16))[2:]

  return

# Creates key and splits into a table
keyList = textwrap.fill(hex(genKey(128))[2:], 2).split('\n')
key = [[], [], [], []]

print("KEY:")
for i in range(4):
  key[i] = keyList[i:i+4]
  print(key[i])

aesEnc(key, 'lol')
