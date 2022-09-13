import numpy as np
import textwrap
import random
import math
import re

# AES -------------------------------------------------------------------------------------------------------
SBOX = [['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76'],
        ['ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0'],
        ['b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15'],
        ['04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'eb', '27', 'b2', '75'],
        ['09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84'],
        ['53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf'],
        ['d0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8'],
        ['51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2'],
        ['cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73'],
        ['60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db'],
        ['e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79'], # A
        ['e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08'],
        ['ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a'],
        ['70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e'],
        ['e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'cE', '55', '28', 'df'],
        ['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16']]
                                                                      #A
RCON = ['00000000', '01000000', '02000000', '04000000', '08000000', '10000000', '20000000', '40000000', '80000000', '1B000000', '36000000']

# Convert string to a 4x4 grid
def strToGrid(str: str) -> list:
  strList = textwrap.fill(str, 2).split("\n")
  row = []
  grid = []
  count = 0
  for i in range(16):
    row.append(strList[i])
    count += 1
    if count == 4:
      grid.append(row)
      row = []
      count = 0

  return grid

# Convert 4x4 grid to string
def gridToStr(grid: list) -> str:
  s = list(i for j in grid for i in j)
  s = ''.join(sum(grid, []))
  
  return s

# Special multiplication (Galois Fields)
def gmul(a: int, b: int) -> int:
  if b == 1:
    return a
  tmp = (a << 1) & 0xff
  if b == 2:
    return tmp if a < 128 else tmp ^ 0x1b
  if b == 3:
    return gmul(a, 2) ^ a

# Rotate the last and first positions of a word
def rotWord(row: str) -> str:
  return row[2:] + row[:2]

# Subtraction operation in MixColumns
def subWord(row: str) -> str:
  a = SBOX[int(row[0], 16)][int(row[1], 16)]
  b = SBOX[int(row[2], 16)][int(row[3], 16)]
  c = SBOX[int(row[4], 16)][int(row[5], 16)]
  d = SBOX[int(row[6], 16)][int(row[7], 16)]
  return a + b + c + d

# Key expansion phase in AES
def expandKey(key: str, rounds: int) -> list:
  expandedKey = []
  n = 4 # 4 words for AES-128
  for i in range(4 * rounds):
    value = ""
    if i < n:
      value = key[i]
    elif i >= n and i % n == 0:
      value = f"{int(expandedKey[i - n], 16) ^ int(subWord(rotWord(expandedKey[i - 1])), 16):08x}"
      value = f"{int(value, 16) ^ int(RCON[i // n], 16):08x}"
    elif i >= n and n > 6 and i % n == 4:
      value = f"{int(expandedKey[i - n], 16) ^ int(subWord(expandedKey[i - 1]), 16):08x}"
    else:
      value = f"{int(expandedKey[i - n], 16) ^ int(expandedKey[i - 1], 16):08x}"
    expandedKey.append(value)

  return expandedKey

# RSA -------------------------------------------------------------------------------------------------------

# Modular exponentiation (X^Y % P)
def power(x: int, y: int, p: int) -> int:
  res = 1
  x = x % p

  if (x == 0) :
    return 0

  while (y > 0) :
    if ((y & 1) == 1) :
      res = (res * x) % p
    y = y // 2
    x = (x * x) % p
        
  return res

# B64 -------------------------------------------------------------------------------------------------------
# Zero fill right shift
def zfrs(val: int, n: int) -> int:
  return (val >> n) if val >= 0 else ((val + 0x100000000) >> n)