import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()



def main() -> None:
    """
    Simple terminal chatbot using Groq API.
    - Model: llama-3.3-70b-versatile
    - Keeps full conversation history
    - Type 'exit' to quit
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY environment variable is not set. "
            "Please set it to your Groq API key and run again."
        )

    client = Groq(api_key=api_key)

    # Full conversation history, including system message
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant, answer in simple english.",
        }
    ]

    print("Chatbot is ready. Type 'exit' to end the conversation.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("Chat ended.")
            break

        if not user_input:
            continue

        # Add user message to history
        messages.append({"role": "user", "content": user_input})

        # Call Groq chat completion API
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
        )

        ai_message = response.choices[0].message.content.strip()

        # Add assistant response to history
        messages.append({"role": "assistant", "content": ai_message})

        # Print AI response clearly
        print("\nAI:", ai_message, "\n")


if __name__ == "__main__":
    main()

