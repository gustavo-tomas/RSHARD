from utils import rot, load, store

# SHA3-256 --------------------------------------------------------------------------------------------------
# Permutations (f1600)
def keccak_f(state):
  lanes = [[load(state[8*(x+5*y):8*(x+5*y)+8]) for y in range(5)] for x in range(5)]
  lanes = rounds(lanes)
  state = bytearray(200)
  for x in range(5):
    for y in range(5):
      state[8*(x+5*y):8*(x+5*y)+8] = store(lanes[x][y])
  return state

# Rounds
def rounds(lanes):
  R = 1
  for round in range(24):
    
    # Theta step
    C = [lanes[x][0] ^ lanes[x][1] ^ lanes[x][2] ^ lanes[x][3] ^ lanes[x][4] for x in range(5)]
    D = [C[(x+4)%5] ^ rot(C[(x+1)%5], 1) for x in range(5)]
    lanes = [[lanes[x][y]^D[x] for y in range(5)] for x in range(5)]
    
    # Rho and Phi
    (x, y) = (1, 0)
    current = lanes[x][y]
    for t in range(24):
      (x, y) = (y, (2*x+3*y)%5)
      (current, lanes[x][y]) = (lanes[x][y], rot(current, (t+1)*(t+2)//2))
    
    # Qui
    for y in range(5):
      T = [lanes[x][y] for x in range(5)]
      for x in range(5):
        lanes[x][y] = T[x] ^((~T[(x+1)%5]) & T[(x+2)%5])
    
    # Iota
    for j in range(7):
      R = ((R << 1) ^ ((R >> 7)*0x71)) % 256
      if (R & 2):
        lanes[0][0] = lanes[0][0] ^ (1 << ((1<<j)-1))

  return lanes

# Sponge function
def keccak(rate, capacity, inputBytes, suffix, outputByteLen):
  
  # Initialization
  outputBytes = bytearray()
  state = bytearray([0 for i in range(200)])
  rateInBytes = rate // 8
  blockSize = 0
  if (((rate + capacity) != 1600) or ((rate % 8) != 0)):
    return
  inputOffset = 0

  # Absorbing phase
  while(inputOffset < len(inputBytes)):
    blockSize = min(len(inputBytes)-inputOffset, rateInBytes)
    for i in range(blockSize):
      state[i] = state[i] ^ inputBytes[i+inputOffset]
    inputOffset = inputOffset + blockSize
    if (blockSize == rateInBytes):
      state = keccak_f(state)
      blockSize = 0

  # Padding
  state[blockSize] = state[blockSize] ^ suffix
  if (((suffix & 0x80) != 0) and (blockSize == (rateInBytes-1))):
    state = keccak_f(state)
  state[rateInBytes - 1] = state[rateInBytes - 1] ^ 0x80
  state = keccak_f(state)

  # Squeezing
  while(outputByteLen > 0):
    blockSize = min(outputByteLen, rateInBytes)
    outputBytes = outputBytes + state[0:blockSize]
    outputByteLen = outputByteLen - blockSize
    if (outputByteLen > 0):
      state = keccak_f(state)

  return outputBytes

def sha3_256(inputBytes):
  return keccak(1088, 512, inputBytes, 0x06, 256//8)

# SHA3-256
# inputBytes = bytearray("", "utf-8")
# hashRes = sha3_256(inputBytes)
# print("RES:", hashRes.hex())