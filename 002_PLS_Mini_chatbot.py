def chatbot():
    print("PLS Mini Chatbot")
    print("Type 'exit' to quit\n")

    while True:
        user = input("You: ").lower()

        if user == "exit":
            print("Bot: Bye")
            break

        elif "hello" in user or "hi" in user:
            print("Bot: Hey! How can I help you?")

        elif "your name" in user:
            print("Bot: I'm PLS Bot")

        elif "time" in user:
            from datetime import datetime
            now = datetime.now().strftime("%H:%M:%S")
            print(f"Bot: Current time is {now}")

        elif "python" in user:
            print("Bot: Python is a powerful programming language")

        elif "who created you" in user:
            print("Bot: I was created by Peter Lightspeed")

        else:
            print("Bot: I don't understand yet, but I'm learning")

chatbot()
