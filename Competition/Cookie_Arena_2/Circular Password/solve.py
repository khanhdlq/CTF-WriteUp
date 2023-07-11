def rotate_string(password, rotated_password):
    # Kiểm tra phép xoay xuôi
    for i in range(len(password)):
        if password[i:] + password[:i] == rotated_password:
            return True

    # Kiểm tra phép xoay ngược
    for i in range(len(password)-1, -1, -1):
        if password[i:] + password[:i] == rotated_password:
            return True

    return False

# Đọc dữ liệu đầu vào
password = input()
rotated_password = input()

# Kiểm tra xem mật khẩu mới có thể được sinh ra bằng cách xoay mật khẩu gốc hay không
if rotate_string(password, rotated_password):
    print("MAYBE")
else:
    print("NO")
