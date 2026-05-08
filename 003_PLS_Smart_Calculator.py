def calculator():
    print("PLS Smart Calculator")
    print("Type like: add 5 and 3")
    print("Commands: add, sub, mul, div")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input(">>>>").lower()

        if user_input == "exit":
            print("Goodbye")
            break

        try:
            words = user_input.split()

            operation = words[0]
            num1 = float(words[1])
            num2 = float(words[3])

            if operation == "add":
                result = num1 + num2
            elif operation == "sub":
                result = num1 - num2
            elif operation == "mul":
                result = num1 * num2
            elif operation == "div":
                if num2 == 0:
                    print("Cannot divide by zero")
                    continue
                result = num1 / num2
            else:
                print("Unknown operation")
                continue

            print(f"Result: {result}\n")

        except:
            print("Invalid format. Try: add 5 and 3\n")

calculator()
