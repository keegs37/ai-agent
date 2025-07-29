from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

def call_function(function_call_part, verbose = False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}")
    
    fn = function_call_part.name          
    args = function_call_part.args or {}  # just in case it’s None
    result = None                         # will hold the return value

    if fn == "get_files_info":
        # provide default for optional arg
        directory = args.get("directory") or "."
        result = get_files_info("calculator", directory=directory)

    elif fn == "get_file_content":
        result = get_file_content("calculator", args["file_path"])

    elif fn == "run_python_file":
        extra_args = args.get("args") or []
        result = run_python_file("calculator", args["file_path"], args=extra_args)

    elif fn == "write_file":
        result = write_file("calculator", args["file_path"], args["content"])

    else:  # unknown tool – tell Gemini what went wrong
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=fn,
                    response={"error": f"Unknown function: {fn}"},
                )
            ],
        )

    # --- 2. hand **the result** back to the model ------------------------------
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=fn,
                response={"result": result},   # must be JSON‑serialisable
            )
        ],
    )


'''
# If the AI calls a function, add the function call info to return_string and call the function itself
if response.function_calls:
    for fc in response.function_calls:
        if fc.name == "get_files_info":
            print(f"Calling function: {fc.name}({fc.args})")
            # Check if AI is using the default arg of get_files_info
            if fc.args["directory"] == None:
                print(get_files_info("calculator", directory = "."))
            else:
                print(f"Calling function: {fc.name}({fc.args})")
                print(get_files_info("calculator", directory = fc.args["directory"]))
                
        # Run the specified function if AI calls it, passing AI created args
        if fc.name == "get_file_content":
            print(f"Calling function: {fc.name}({fc.args})")
            print(get_file_content("calculator", fc.args["file_path"]))

        # Run the specified function if AI calls it, passing AI created args
        if fc.name == "run_python_file":
            print(f"Calling function: {fc.name}({fc.args})")
            # Check if AI included optional args
            if len(fc.args) > 1: 
                print(run_python_file("calculator", fc.args["file_path"], args = [fc.args["args"]]))
            else:
                print(run_python_file("calculator", fc.args["file_path"]))

        # Run the specified function if AI calls it, passing AI created args
        if fc.name == "write_file":
            print(f"Calling function: {fc.name}({fc.args})")
            print(write_file("calculator", fc.args["file_path"], fc.args["content"]))
'''