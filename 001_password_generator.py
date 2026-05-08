# Project 1, follow Peter Lightspeed for more!
import random
import string
def generate_password(length):
    # Combine all characters: a-z, A-Z, 0-9, and symbols
    characters = string.ascii_letters + string.digits + string.punctuation

    # Generate password by randomly choosing characters
    password = ''.join(random.choice(characters) for _ in range(length))
    return password
# Get input and generate
try:
    length = int(input("Enter password length: "))
    if length < 8:
        print("Length must be at least 8.")
    else:
        print("Generated Password:", generate_password(length))
except ValueError:
    print("Please enter a valid number.")
