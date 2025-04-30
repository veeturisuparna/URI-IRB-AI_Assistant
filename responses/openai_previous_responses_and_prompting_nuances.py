#openai_previous_responses_and_prompting_nuances.py
from openai import OpenAI

client = OpenAI()

def explore_multiple_instructions():
    print("\n=== Exploring multiple instructions with previous responses ===")
    
    # Initial response with first instruction and system message
    """We can see when running this code that each message is stored as a separate object in the list of the inputs that go into
    the next response, however, the system prompts aren't treated in the same manner as the instructions field specifically itself.
    We can see that the actual system prompts within the input continuously stay within the chain of responses but the instructions do not
    """
    initial_response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            
            {"role": "system", "content": "You are a poetic writer."},
            {"role": "system", "content": "You must include sensory details."},
            {"role":"user", "content": "Write about a garden."}
        ],
        instructions="Write in short, vivid sentences.",
        store=True
    )   
    
    print("===================================================")
    print(f"Initial Response")
    print("===================================================")
    
    print(f"Initial Instructions: {initial_response.instructions}")
    
    print(f"Initial Inputs: ")
    messages = client.responses.input_items.list(initial_response.id).data
    for i, msg in enumerate(messages):
        print(f"\nMessage {i+1}:")
        print(f"Content: {msg}")
        print(f"Type: {type(msg)}")
    
    print("\nFirst response (with multiple system messages and instruction):")
    print(initial_response.output_text)
    
    # Second response using previous response but no new instructions
    second_response = client.responses.create(
        model="gpt-4o-mini",
        input="Now describe the garden in winter.",
        previous_response_id=initial_response.id,
        store=True
    )
    
    print("===================================================")
    print(f"Second Response")
    print("===================================================")

    print("\nChecking if original instructions persisted:")
    print(f"Instructions: {second_response.instructions}")
    
    print(f"Initial Inputs: ")
    messages = client.responses.input_items.list(second_response.id).data
    for i, msg in enumerate(messages):
        print(f"\nMessage {i+1}:")
        print(f"Content: {msg}")
        print(f"Type: {type(msg)}")
        
    print("\nSecond response (using previous response, no new instructions):")
    print(second_response.output_text)

    
    # Third response with new instruction but keeping previous response
    third_response = client.responses.create(
        model="gpt-4o-mini",
        input="Describe the garden as if it were on fire.",
        #Uncomment this to see the difference in the response when the instructions are changed, if there is any
        # instructions="Write only in metaphors.",
        previous_response_id=second_response.id,
        store=True
    )
    
    print("===================================================")
    print(f"Final Response")
    print("===================================================")
    
    print(f"Final Instructions: {third_response.instructions}")

    print("\nChecking final message chain:")
    message = client.responses.input_items.list(third_response.id)
    for i, msg in enumerate(message.data):
        print(f"\nMessage {i+1}:")
        print(f"Content: {msg}")
        print(f"Type: {type(msg)}")
    

    print("\nThird response (new instruction, using previous response):")
    print(third_response.output_text)


# Run the exploration
explore_multiple_instructions()


