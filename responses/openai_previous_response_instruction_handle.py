from openai import OpenAI

client = OpenAI()

"""
This module demonstrates how instructions are handled in the OpenAI Responses API, particularly
in multi-turn conversations. Key points about instruction handling:

1. Instructions are not preserved between responses like conversation history
2. Each new response can have its own instruction that overrides previous ones
3. Only the most recent instruction is active for the current response
4. Unlike system messages which persist in the conversation chain, instructions are ephemeral
"""

def demonstrate_instruction_handling():
    print("\n=== Demonstrating instruction handling with previous responses ===")
    
    # Initial response with first instruction
    # The instruction "Write only in haiku format" will only apply to this response
    # It is not stored as part of the conversation history
    initial_response = client.responses.create(
        model="gpt-4o-mini",
        input="Write a haiku about Paris.",
        instructions="Write only in haiku format.", # This instruction only affects this response
        store=True  # Storing allows this response to be referenced later
    )
    
    # We can inspect the current instruction, but this will not be available 
    # in subsequent responses unless explicitly set again
    print("\nInspecting current conversation iteration instructions:")
    instructions = initial_response.instructions
    print(f"Instructions: {instructions if instructions else 'No instructions'}")
    
    print("\nFirst response (with haiku instruction):")
    print(initial_response.output_text)
    
    
    # Second response uses previous_response_id to maintain conversation context
    # But sets a new instruction that completely replaces the haiku instruction
    # The model will now ignore the previous haiku instruction and only follow
    # the new prose format instruction
    second_response = client.responses.create(
        model="gpt-4o-mini",
        input="Now describe what you wrote about Paris.",
        instructions="Write in prose format only.", # New instruction overrides previous
        previous_response_id=initial_response.id,  # Links conversation but NOT instructions
        store=True
    )
    
    print(second_response)
    
    # Demonstrating that only the most recent instruction is accessible
    # The haiku instruction from the first response is not preserved
    print("\nInspecting current conversation iteration instructions:")
    instructions = second_response.instructions
    print(f"Instructions: {instructions if instructions else 'No instructions'}")
    
    print("\nSecond response (with prose instruction):")
    print(second_response.output_text)
    
    """ 
    Examining the conversation objects to show that while message history is preserved,
    instructions are not part of the conversation chain. System messages and user/assistant
    interactions are stored, but instructions are handled separately for each response.
    """
    messages = client.responses.input_items.list(second_response.id).data
    for i, msg in enumerate(messages):
        print(f"\nMessage {i+1}:")
        print(f"Content: {msg}")
        print(f"Type: {type(msg)}")

# Run the demonstration
demonstrate_instruction_handling()