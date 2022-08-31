from part1 import genKey

def main():
  
  mrKey = genKey(1024)
  print("KEY:", hex(mrKey))

if __name__ == "__main__":
    main()
