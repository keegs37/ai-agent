import os
import subprocess
def run_python_file(working_directory, file_path, args=[]):
    requested_file = os.path.join(os.path.abspath(working_directory), file_path)

    # Prevent directory traversal outside of working directory
    if os.path.abspath(working_directory) not in os.path.abspath(requested_file):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isfile(os.path.abspath(requested_file)) == False:
        return f'Error: File "{file_path}" not found.'

    
    if file_path[len(file_path) - 3:len(file_path)] != ".py":
        return f"Error: '{file_path}' is not a Python file."
    
    # Setting commands for subprocess.run including the file to run
    command = ["python", os.path.abspath(requested_file)] + args
    subprocess.run(command, stdin = True, stdout = True, timeout = 30, cwd = os.path.abspath(working_directory))

print(run_python_file("calculator", "main.py",["3 + 2"]))