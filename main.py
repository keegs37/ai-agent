import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv

system_prompt = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""
# Load api key and initialize the ai client
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Check if a prompt was provided, error if not
if len(sys.argv) < 2:
    print('Error: No prompt provided. Usage: python3 main.py "Your prompt here"')
    sys.exit(1)

# Pass the user prompt from cli to make a Content instance 
user_prompt = sys.argv[1]
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

# Pass user prompt to the AI model and capture the response
response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt)
)
# List for return string 
return_string = []

# Add AI response to return_string
return_string.append(response.text)

# If there are no "--" flags return the AI respond only
if len(sys.argv) < 3:
    print("\n".join(return_string))
    sys.exit()

# If --verbose flag is used return more info
if "--verbose" in sys.argv[2]:
    return_string.append(f"User prompt: {sys.argv[1]}")
    return_string.append(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    return_string.append(f"Response tokens: {response.usage_metadata.candidates_token_count}")

print("\n".join(return_string))