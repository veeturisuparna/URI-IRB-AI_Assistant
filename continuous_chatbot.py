# continuous_chatbot.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Get API key
api_key = os.getenv('OPENAI_API_KEY')

# Check if API key exists
if not api_key:
    print("Error: OPENAI_API_KEY not found in environment variables.")
    exit(1)

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

print("Welcome to the Continuous Chatbot! Type 'quit' to exit.\n")

# Initialize context and turn counter
previous_response_id = None
turn_count = 0

while True:
    turn_count += 1

    if turn_count % 3 == 0:
        print("\n--- Forced Turn ---")
        user_input = input("Chatbot asks: Any specific topic you'd like to explore? > ")
    else:
        user_input = input("You: ")

    if user_input.lower() == 'quit':
        print("Exiting chatbot. Goodbye!")
        break

    try:
        print("Chatbot is thinking...")

        api_args = {
            "model": "gpt-4o-mini",
            "input": user_input,
            "store": True
        }

        if previous_response_id:
            api_args["previous_response_id"] = previous_response_id

        response = client.responses.create(**api_args)
        response_text = response.output_text

        print("Chatbot:", response_text)
        previous_response_id = response.id

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        previous_response_id = None  # Optional context reset
