#!/usr/local/bin/python
# -*- coding: utf-8 -*-

def main():
  password = "with open('ten_file.txt', 'r') as file: print(file.read())aaa" 
  inp = input("Enter a Python list: ")
  lis = eval(inp, {'__builtins__': None}, None)
  if type(lis) != list:
    print("That's not a list")
    return
  for i in lis:
    if not isinstance(i, int):
      print("The list can only contain integers")
      return
  ord_list = [ord(e) for e in password]  # Tạo danh sách từ biểu thức [ord(e) for e in password]
  print("List created from the password expression:", ord_list)

  if lis == ord_list:
    print("You are now authorized!")
    with open("flag.txt", "r") as flag:
      print(flag.read())
  else:
    print("Incorrect password!")

if __name__ == "__main__":
  main()

