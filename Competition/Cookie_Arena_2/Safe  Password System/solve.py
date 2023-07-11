def is_secure_password(password):
    if len(password) < 8:
        return "NO"

    lowercase = False
    uppercase = False
    digit = False
    special_char = False

    for char in password:
        if char.islower():
            lowercase = True
        elif char.isupper() and password.index(char) != 0 and password.index(char) != len(password) - 1:
            uppercase = True
        elif char.isdigit() and password.index(char) != 0 and password.index(char) != len(password) - 1:
            digit = True
        elif char in ['@', '#', '$', '&']:
            special_char = True

    if lowercase and uppercase and digit and special_char:
        return "YES"
    else:
        return "NO"

# Nhập số lượng test
n = int(input())
password = [] 
# Duyệt qua từng test
for i in range(n):
    password.append(input())
for i in range(n):
    result = is_secure_password(password)
    print(result)
#cooKIE#P1
#U@arena4HNO
