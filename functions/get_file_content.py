import os
from functions.config import MAX_CHARACTERS
from google.genai import types
def get_file_content(working_directory, file_path):
    # File to list the contents of
    requested_file = os.path.join(working_directory, file_path)
    
    try:
        # Prevent directory traversal outside the working directory
        if os.path.abspath(working_directory) not in os.path.abspath(requested_file):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        # Verify the requested file is an actual file
        if os.path.isfile(requested_file) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
    
        # Open file, and return contents truncated to MAX_CHARACTERS value (10,000) if applicable
        with open(requested_file, 'r') as file:
            content = file.read()
            if len(content) > MAX_CHARACTERS:
                return f"{content[:MAX_CHARACTERS]} [...File {os.path.abspath(requested_file)} truncated at 10000 characters]"

            return content

    # Return error message if any standard library call fails
    except Exception as e:
        return f"Error: {e}"

# Schema telling the AI how to use the function 
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Opens a specified file and returns its contents truncated to 10,000 characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file name you want to see the contents of",
            ),
        },
    ),
)