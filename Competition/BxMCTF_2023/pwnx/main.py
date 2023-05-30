#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from pwn import*
def main():
  password = "the password can contain non-ascii charactérs :)"
  inp = b"khanh"
  lis = eval(inp, {'__builtins__': None}, None)
  if type(lis) != list:
    print("That's not a list")
    return
  for i in lis:
    if not isinstance(i, int):
      print("The list can only contain integers")
      return
  if lis == [ord(e) for e in password]:
    print("You are now authorized!")
    with open("flag.txt", "r") as flag:
      print(flag.read())
  else:
    print("Incorrect password!")

if __name__ == "__main__":
  main()
