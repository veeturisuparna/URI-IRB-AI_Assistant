#openai_basic_response_test.py
from openai import OpenAI
from dotenv import load_dotenv
import os

#this statement lets us use the .env file to store our API key
#but it also allows any new values for the environment variables to
#be automatically used within our script/program
load_dotenv(override=True)

client = OpenAI(
    #This argument is actually already included whenever we simply call OpenAI()
    #for the definition of the OpenAI object's constructor, this is set as the 
    #default value of the api_key parameter.
    api_key=os.getenv("OPENAI_API_KEY")
)

response = client.responses.create(
  model="gpt-4o-mini",
  input="Tell me a three sentence bedtime story about a unicorn."
)

"""

For the response API the breakdown of how a response is structured follows the examples below on how to 
access the different parts of the response.

"""


"""
This is the raw full response object from the OpenAI API. This level includes metadata about the response including it's specific id
alongside time of creation, instructions used to make it, model, and if there are any specific errors associated with the API call.

Response(id='resp_67d34628bc008190821a85777e9a27c5027839ba519431db', created_at=1741899304.0, error=None, 
incomplete_details=None, instructions=None, metadata={}, model='gpt-4o-mini-2024-07-18', object='response', 
output=[ResponseOutputMessage(id='msg_67d346296dd48190af99d1b864afe461027839ba519431db', 
content=[ResponseOutputText(annotations=[], text='Once upon a time, in a shimmering forest, 
a kind-hearted unicorn named Luna helped lost animals find their way home with her glittering horn. 
One starry night, she discovered a lonely little star that had fallen from the sky, so she gently 
guided it back to its place among the constellations. As a thank-you, the star showered Luna with 
sparkles, ensuring her forest would always shine bright and be filled with magic.', type='output_text')], 
role='assistant', status='completed', type='message')], parallel_tool_calls=True, temperature=1.0, 
tool_choice='auto', tools=[], top_p=1.0, max_output_tokens=None, previous_response_id=None, 
reasoning=Reasoning(effort=None, generate_summary=None), status='completed', 
text=ResponseTextConfig(format=ResponseFormatText(type='text')), truncation='disabled', 
usage=ResponseUsage(input_tokens=36, output_tokens=90, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), 
total_tokens=126, input_tokens_details={'cached_tokens': 0}), user=None, store=True)
"""

print(response)

print("-------------------------------- ")


""" 
This is the first message output object from the response. This level includes the message id, content, role, status, and type.

ResponseOutputMessage(id='msg_67d346296dd48190af99d1b864afe461027839ba519431db', 
content=[ResponseOutputText(annotations=[], text='Once upon a time, in a shimmering forest, 
a kind-hearted unicorn named Luna helped lost animals find their way home with her glittering horn. 
One starry night, she discovered a lonely little star that had fallen from the sky, so she gently 
guided it back to its place among the constellations. As a thank-you, the star showered Luna with 
sparkles, ensuring her forest would always shine bright and be filled with magic.', type='output_text')], 
role='assistant', status='completed', type='message')
"""

print(response.output[0])

print("-------------------------------- ")


"""
This is the text content of the first message from the response. This level includes the text, type, and annotations.

ResponseOutputText(annotations=[], text='Once upon a time, in a shimmering forest, 
a kind-hearted unicorn named Luna helped lost animals find their way home with her 
glittering horn. One starry night, she discovered a lonely little star that had fallen 
from the sky, so she gently guided it back to its place among the constellations. As a 
thank-you, the star showered Luna with sparkles, ensuring her forest would always shine 
bright and be filled with magic.', type='output_text')
"""

print(response.output[0].content[0])

print("-------------------------------- ")


"""
This is the text content of the first message from the response which is purely the response of the OpenAI model itself.

Once upon a time, in a shimmering forest, a kind-hearted unicorn 
named Luna helped lost animals find their way home with her glittering horn. 
One starry night, she discovered a lonely little star that had fallen from the sky, 
so she gently guided it back to its place among the constellations. As a thank-you, 
the star showered Luna with sparkles, ensuring her forest would always shine bright 
and be filled with magic.
"""

print(response.output[0].content[0].text)

print("-------------------------------- ")

"""
This is the simplification of the response text utilizing the response.output_text helper which dramatically 
reduces the amount of text returned and fields which need to be parsed in order to get the response text.


Once upon a time, in a shimmering forest, a kind-hearted unicorn 
named Luna helped lost animals find their way home with her glittering horn. 
One starry night, she discovered a lonely little star that had fallen from the sky, 
so she gently guided it back to its place among the constellations. As a thank-you, 
the star showered Luna with sparkles, ensuring her forest would always shine bright 
and be filled with magic.
"""

print(response.output_text)