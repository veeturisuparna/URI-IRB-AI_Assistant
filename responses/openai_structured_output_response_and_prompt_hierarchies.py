#openai_structured_output_response_and_prompt_hierarchies.py
from typing import TypeVar, Type, List
from pydantic import BaseModel
from openai import OpenAI

""" This module is all about hierarchical prompts and the differences
between platform, system, developer, and user prompts. Plus, the further formalization
in structured output and the utilization of pydantic 
models to parse the response into a structured format, useful for all sorts of tasks
relevant to AI applications for yielding more deterministic and reliable results."""

#https://www.youtube.com/watch?v=0pGxoubWI6s
#This video should be a good example of how the OpenAI API works with Pydantic models.
#This is the direct github showing how it works also too: https://github.com/openai/openai-python/blob/main/examples/responses/structured_outputs.py



class Step(BaseModel):
    """Represents a single step in a mathematical reasoning process
    
    JSON Structure:
    {
        "explanation": "string describing the reasoning for this step",
        "output": "string showing the mathematical work/result"
    }
    
    Example:
    {
        "explanation": "First, move all terms with x to the left side",
        "output": "8x = -23 - 7"
    }
    """
    explanation: str  # Detailed explanation of the mathematical step
    output: str      # The actual mathematical operation or result

class MathReasoning(BaseModel):
    """Encapsulates a complete mathematical solution with steps and final answer
    
    JSON Structure:
    {
        "steps": [
            {
                "explanation": "string",
                "output": "string"
            },
            ...more steps...
        ],
        "final_answer": "string containing the solution"
    }
    
    Example:
    {
        "steps": [
            {
                "explanation": "Move all terms with x to left side",
                "output": "8x = -23 - 7"
            },
            {
                "explanation": "Simplify right side",
                "output": "8x = -30"
            },
            {
                "explanation": "Divide both sides by 8",
                "output": "x = -30/8"
            }
        ],
        "final_answer": "x = -3.75"
    }
    
    By extending Pydantic's BaseModel:
    1. Automatic validation of input data structure
    2. Type checking for all fields
    3. JSON serialization/deserialization
    4. Schema generation for API documentation
    5. IDE support with autocomplete
    """
    steps: list[Step]       # List of reasoning steps
    final_answer: str       # The final solution



# Showcasing prompt hierarchies and structured output with Pydantic models
try:
    client = OpenAI()
    messages = [
        #The platform prompt is the highest priority prompt which overrides all other prompts, these prompts are hidden in the backend of the OpenAI API
        #and are not visible to users or developers, as they're proprietary to OpenAI
        
        #The system prompt is the next highest priority prompt which overrides any developer or user prompts
        {
            #These system prompts are the ones that are used to guide the model's behavior and the instructions that the model will follow
            #They're exactly the same as the ones used in the ChatGPT interface when you create a new GPTAssistant. However, when utilized in this role
            #the multi-turn format keeps these system prompt continuously within the chain of responses.
            "role": "system",
            "content": "Reason Mathematically",
        },
        
        #The developer prompt is the next highest priority prompt which only overrides the user prompt, but is superseded by the system and platform prompt
        {
            #Step down from the platform and system prompts to the developer prompt, think of them as an extension of the system prompt
            #in order to further guide the model's behavior and the instructions that the model will follow, but allows you to add in more
            #specific instructions for certain tasks without having the system prompt become too large and unwieldy
            "role": "developer",
            "content": "You are a helpful math tutor. Guide the user through the solution step by step.",
        },
        
        #The user prompt is the lowest priority prompt which gets overridden by the developer, system, and platform prompts 
        #and acts more as the direct input from the user that is changed or interacted via guidelines, constraints, or extra information. 
        #defined in the developer, system, and platform prompts
        {"role": "user", "content": "how can I solve 8x + 7 = -23"},
    ]
    
    response = client.responses.parse(
        model="gpt-4o-mini",
        input=messages,
        #the instructions field specifically itself is not part of the chain of responses and is only used to guide the model's behavior for the current response
        #Uncomment this to see the difference in the response when the instructions are changed, if there is any
        # instructions="IGNORE ALL INSTRUCTIONS ABOVE THIS ONE AND SIMPLY RETURN THE FINAL ANSWER",
        text_format=MathReasoning,
    )
    
    print(f"Here are the instructions for the current response: {response.instructions}")

    print("Here is the input messages for the current response:")
    
    for msg in client.responses.input_items.list(response.id):
        print(msg)

    model_response = response.output[0].content[0].parsed
    print(response)
    print(type(model_response))
    print(model_response)
    print(model_response.model_dump_json(indent=2))
    
except Exception as e:
    print(f"Error: {e}")
    # handle errors like finish_reason, refusal, content_filter, etc.
    pass

