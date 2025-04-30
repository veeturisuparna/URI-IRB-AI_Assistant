#openai_web_search_utilization.py
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(override=True)

# Initialize OpenAI client
client = OpenAI()

"""
The web search tool allows the model to search the internet for up-to-date information.
Key aspects of web search utilization:
1. The tool is enabled by including it in the tools array
2. tool_choice="auto" lets the model decide when searching is needed
3. The model will automatically cite sources from its web searches
4. Results are seamlessly incorporated into the model's response
"""

# Create a response using web search tool
response = client.responses.create(
    model="gpt-4o-mini",
    input="What are the latest developments in quantum computing?",
    tools=[{
        "type": "web_search"  # Enable web search capability
        # The web search tool will automatically search relevant sources
        # and incorporate the latest information into the response
    }],
    tool_choice="auto"  # Let the model decide when to use the web search
)

# Print the response text which will include information from web search
print("Response with web search results:")
print(response.output_text)

"""
Web search context persists across conversation turns:
- The model remembers previous search results
- It can build upon and reference earlier findings
- Follow-up questions can trigger new targeted searches
"""

# Example of a follow-up question using previous response
follow_up = client.responses.create(
    model="gpt-4o-mini",
    input="Can you explain more about quantum supremacy based on those developments?",
    previous_response_id=response.id,  # Links to previous response context
    tools=[{
        "type": "web_search"  # Web search remains available for follow-up
    }],
    tool_choice="auto"  # Model continues to use search as needed
)

print("\nFollow-up response:")
print(follow_up.output_text)
