import time
import random

def function1(a1, a2):
    v3 = 0
    i = 1
    while a1 >= i or a2 >= i:
        if a1 % i == 0 and a2 % i == 0:
            v3 = i
        i += 1
    return v3


def function2(a1):
    if a1:
        return a1 * function2(a1 - 1)
    else:
        return 1

def main():
    v7 = 1
    v13 = int(input())
    v14 = int(input())
    print(v13, v14)
    v4 = function1(v13, v14)
    v5 = function2(v4 + 3)
    print(v5)
    v11 = int(input())
    if v5 != v11:
        v7 = 0


    if v7 == 1:
        print("Whooaaaa! That was quick :D - here's a flag for your efforts:")

if __name__ == "__main__":
    while(1):
        main()
