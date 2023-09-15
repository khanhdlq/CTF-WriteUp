import itertools
import string

# Define the characters to choose from
characters = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'

# Generate and print all 6-character combinations
combinations = itertools.product(characters, repeat=6)
for combo in combinations:
    password = ''.join(combo)
    print(password)
