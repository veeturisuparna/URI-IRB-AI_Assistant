#openai_multi_turn_response_test.py
"""
Multi-Turn Response API Example
=============================

This example demonstrates how to use OpenAI's Response API for multi-turn conversations.
Key aspects of multi-turn conversations:

1. Message Structure
   - Each message in the conversation is a dictionary with 'role' and 'content'
   - Roles can be either 'user' or 'assistant'
   - Messages are ordered chronologically in an array

2. Conversation History
   - Previous messages provide context for the model
   - The model can reference earlier parts of the conversation
   - This enables follow-up questions and contextual understanding

3. Turn Taking
   - Conversations alternate between user and assistant roles
   - Each response from the model considers the full conversation history
   - This creates a coherent, contextual dialogue

4. Initial Seeding
   - You can "seed" a conversation with previous exchanges
   - This lets you start from a specific point in a conversation
   - Useful for continuing previous conversations or setting context

Usage Benefits:
- Maintains conversation context without managing state yourself
- Enables natural follow-up questions
- Allows for complex multi-step interactions
- Can be used to create interactive chatbots or conversation agents
"""

from openai import OpenAI
client = OpenAI()

# Create a multi-turn conversation with the Response API
# Each message dictionary represents one turn in the conversation
response = client.responses.create(
    model="gpt-4o-mini",
    input=[
        # First turn: User provides initial prompt
        {
            "role": "user",
            "content": "Write a one-sentence bedtime story about a unicorn."
        },
        # Second turn: Assistant's response to the story request
        {
            "role": "assistant",
            "content": "Once upon a time, in a shimmering forest, a kind-hearted unicorn named Luna helped lost animals find their way home with her glittering horn."
        },
        # Third turn: User asks a follow-up question about the story
        {
            "role": "user",
            "content": "What is the main character's name?"
        },
    ]
)

# Print the assistant's response to the follow-up question
print(response.output_text)
