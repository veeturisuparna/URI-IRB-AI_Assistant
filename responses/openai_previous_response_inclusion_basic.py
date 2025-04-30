#openai_previous_response_inclusion_basic.py
from openai import OpenAI

"""
Previous Response Inclusion Example
=================================

This example demonstrates how to use OpenAI's Response API with previous_response_id
to create multi-turn conversations in a simpler way than manually tracking message history.

Key differences from multi-turn conversations:
1. No need to manually construct message arrays
2. Previous context is automatically handled by OpenAI
3. More streamlined API for continuing conversations
4. Requires responses to be stored (store=True by default)

The flow works like this:
1. Make initial response call
2. Get response.id
3. Use that id in subsequent calls via previous_response_id
4. OpenAI automatically includes prior context
"""
"""
Behind the scenes, using previous_response_id is equivalent to the multi-turn format:
{
    "role": "user",
    "content": "What is the capital of France?"
}
{
    "role": "assistant",
    "content": "<first response>"
}
{
    "role": "user", 
    "content": "Now explain when it became known..."
}

The API handles this conversion automatically, making code simpler and more maintainable.
"""



client = OpenAI()

# Initial response - asks a simple factual question
# This response will be stored by default (store=True) so we can reference it later
response = client.responses.create(
    model="gpt-4o-mini",
    input="What is the capital of France?"
)

print(response.output_text)

# Second response - follows up on the first response
# Uses previous_response_id to maintain conversation context
# OpenAI will automatically include the previous question and answer
# store=False means this response won't be stored for future reference
second_response = client.responses.create(
    model="gpt-4o-mini",
    previous_response_id=response.id,  # Links this response to the previous one
    input="Now explain when it became known as the capital of France and if there were any other cities that were considered for the title.",
    store=False  # Won't be stored for future reference
)

print(second_response.output_text)

#UNCOMMENT TO SEE ERROR WHEN WE DON'T HAVE THE STORE FIELD SET TO TRUE (LIKE IT DEFAULTS TO)
# This section demonstrates what happens when trying to reference an unstored response
# Since second_response had store=False, trying to reference it will cause an error

# user_response = "What is the capital of France?"
# previous_text_response = second_response.output_text

# third_response = client.responses.create(
#     model="gpt-4o-mini",
#     previous_response_id=second_response.id,  # This will fail because second_response wasn't stored
#     input= user_response + previous_text_response #"What is the capital of France?"
# )

# print(third_response)





"""
This example demonstrates the handling of context accumulation and truncation in multi-turn conversations.

Key concepts:

1. Context Accumulation
   - Each response builds on previous responses through previous_response_id
   - Messages accumulate in two distinct types:
     a) Data Messages (User Input):
        - Raw text inputs from the user
        - Stored with role="user" 
        - Represent the human side of conversation
        - Example: Initial questions and follow-up prompts
     
     b) Response Messages (LLM Output):
        - Generated content from the model
        - Stored with role="assistant"
        - Represent the AI's responses
        - Include both direct answers and reasoning
   
2. Truncation Behavior
   - Without Truncation (truncation='disabled'):
     * Context grows unbounded
     * Eventually hits token limits
     * Fails with context length error
     * Preserves complete conversation history
   
   - With Truncation (truncation='auto'):
     * Automatically manages context length
     * Removes oldest messages first
     * Maintains recent context
     * Allows indefinite conversation
     * May lose historical context
     
3. Message Storage
   - store=True required for context tracking
   - Enables message history retrieval
   - Allows previous_response_id linking
   - Critical for multi-turn functionality

"""

# Test pushing context limits with multiple responses
print("\nTesting context limits with multiple responses...")

def generate_responses(truncate=False):
    # Initial response
    current_response = client.responses.create(
        model="gpt-4o-mini",
        input="Tell me about the history of Paris in 2-3 sentences.",
        store=True
    )
    print("\nInitial Response:")
    print(current_response.output_text)
    
    # Keep track of response count
    response_count = 1
    
    try:
        while True:
            # Create follow-up response this way, we can see the continually accumulation
            #between the interactions of user and assistant roles.
            current_response = client.responses.create(
                model="gpt-4o-mini",
                previous_response_id=current_response.id,
                input=f"Continue telling me more about Paris's history.",
                store=True,
                truncation='auto' if truncate else 'disabled'
            )
            
            # Print all messages in the conversation so far
            messages = client.responses.input_items.list(current_response.id).data
            print("\nConversation history:")
            
            #This conversation history goes back and forth between the Data Message sent by a user side
            #and the Response Message sent by the assistant side.
            for i, msg in enumerate(messages):
                print(f"\n[Turn {i+1}]")
                print(f"Role: {msg.role}")
                print(f"Content: {msg.content}")
            print("\n---")
            
            print(f"\nResponse #{response_count + 1}:")
            print(current_response.output_text)
            response_count += 1
            
    except Exception as e:
        print(f"\nReached limit after {response_count} responses")
        print(f"Error: {str(e)}")

# print("\n=== Without truncation ===")
# generate_responses(truncate=False)

print("\n=== With truncation enabled ===")
generate_responses(truncate=True)



