import re

print("PLS Password Strength Checker")

while True:
    password = input("\nEnter your password: ")

    strength = 0

    # Length check
    if len(password) >= 8:
        strength += 1

    # Uppercase
    if re.search(r"[A-Z]", password):
        strength += 1

    # Lowercase
    if re.search(r"[a-z]", password):
        strength += 1

    # Number
    if re.search(r"[0-9]", password):
        strength += 1

    # Special character
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        strength += 1

    # Results
    if strength <= 2:
        print("Weak Password")
    elif strength == 3 or strength == 4:
        print("Medium Password")
    else:
        print("Strong Password")

    again = input("\nCheck another password? (yes/no): ")

    if again.lower() != "yes":
        print("Goodbye!")
        break
