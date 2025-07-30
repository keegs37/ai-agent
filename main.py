import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file
from functions.call_function import call_function


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

"""

# Exposing the available functions to the AI
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, 
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)
# Load api key and initialize the ai client
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Check if a prompt was provided, error if not
if len(sys.argv) < 2:
    print('Error: No prompt provided. Usage: python3 main.py "Your prompt here"')
    sys.exit(1)

# Pass the user prompt from cli to make a Content object 
user_prompt = sys.argv[1]
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

for i in range(20):
    try:
        # Pass user prompt to the AI model and capture the response
        response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages,
        config=types.GenerateContentConfig(tools = [available_functions], system_instruction=system_prompt))
     
        
        # Add response variations to our conversation list "messages"
        for candidate in response.candidates:
            messages.append(candidate.content)

        # If the AI calls a function run it and return its result, error if the function fails
        if response.function_calls:
            for fc in response.function_calls:

                result = call_function(fc)
                # Add the result of each function call to the conversation list "messages"
                messages.append(result)  
        
                #if not result.parts[0].function_response.response:
                    #raise Exception("Functioned call failed")
                #else:
                    #print(f"-> {result.parts[0].function_response.response}") 
        else: 
            if response.text:
                print(response.text)
            break

    except Exception as e:
        print(f"Error: {e}")
# Add AI response to return_string if there is one          
#if response.text:
    #return_string.append(response.text)

# If there are no "--" flags return the AI response only
#if len(sys.argv) < 3:
    #print("\n".join(return_string))
    #sys.exit()


# If --verbose flag is used return more info
if "--verbose" in sys.argv:
    print(f"User prompt: {sys.argv[1]}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

#print("\n".join(return_string))