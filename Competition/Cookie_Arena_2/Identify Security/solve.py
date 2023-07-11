def identify_input(input_string):
    # Kiểm tra nếu chuỗi chứa ký tự '@', xem nó có phải là địa chỉ email hay không
    if '@' in input_string:
        return 0 # email
    else:
        return 1 # sđt
    
def phone_sec(input_string):
    if len(input_string) >= 5:
        secure_string = input_string[:2] + '*' * (len(input_string) - 5) + input_string[-3:]
        return secure_string

def email_sec(input_string):
    if "@" in input_string:
        username, domain = input_string.split("@")
        if len(username) > 7:
            secured_username = username[:2] + "*" * (len(username) - 5) + username[-3:]
        else:
            secured_username = username[0] + "*" * (len(username) - 2) + username[-1]
        secured_email = secured_username + "@" + domain
        return secured_email
    
resume = []
n = int(input())

for i in range(n):
    string = input()
    if identify_input(string) == 1:
        resume.append(phone_sec(string))
    else:
        resume.append(email_sec(string))

for i in range(n):
    print(resume[i])


