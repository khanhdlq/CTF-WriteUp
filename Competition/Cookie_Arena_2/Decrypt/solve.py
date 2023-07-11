def find_divisors(n):
    divisors = []
    for i in range(1, n + 1):
        if n % i == 0:
            divisors.append(i)
    return divisors

def reverse_string_prefix(n, string):
    reversed_string = string[:n][::-1] + string[n:]  # Đảo ngược n ký tự đầu tiên và ghép với phần còn lại của chuỗi
    return reversed_string

# Số nguyên n và chuỗi cần đảo ngược
n = int(input())
divisors = find_divisors(n)
reversed_string = input()
# Gọi hàm reverse_string_prefix để đảo ngược n ký tự đầu tiên của chuỗi
for i in range(len(divisors)):
    reversed_string = reverse_string_prefix(divisors[i], reversed_string)

print(reversed_string)