from ollama_system_user_prompt import get_response

def main():
    messages = [

        {
            "role": "system",
            "content": "You are a interview preparation assistant."

        }
    ]
    print("Gemma chat started. Type 'exit' to stop.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("\n Thanks you....")
            break;
        messages.append({"role": "user", "content": user_input})
        response = get_response(messages)
        messages.append({"role": "assistant", "content": response})
        print("Assistant:", response)
    print("Welcome to the Ollama chat client!")


if __name__ == "__main__":
    main()

