import os
import subprocess
def run_python_file(working_directory, file_path, args=[]):
    requested_file = os.path.join(os.path.abspath(working_directory), file_path)
    try:

        # Prevent directory traversal outside of working directory
        if os.path.abspath(working_directory) not in os.path.abspath(requested_file):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        # Check to see if the file exists
        if os.path.isfile(os.path.abspath(requested_file)) == False:
            return f'Error: File "{file_path}" not found.'

        # Make sure the file is a .py file 
        if file_path[len(file_path) - 3:len(file_path)] != ".py":
            return f"Error: '{file_path}' is not a Python file."
        
        # Setting commands for subprocess.run including the file to run
        command = ["python", os.path.abspath(requested_file)] + args
        # Run the requested file with a timeout of 30 seconds, capture std in and out and run in the working_directory
        process = subprocess.run(command, capture_output = True, text = True, timeout = 30, cwd = os.path.abspath(working_directory))
        
        # List to store return values
        return_string = []

        # Add stdout and stderr to the return string 
        return_string.append(f"STDOUT: {process.stdout}")
        return_string.append(f"STDERR: {process.stderr}")

        # Check if there were errors or no output and return values accordingly
        if process.returncode > 0:
            return_string.append(f"Process exited with code {process.returncode}")
        if not process.stdout:
            return_string.append("No output produced") 
        return "\n".join(return_string)

    # Return error message if any standard library call fails
    except Exception as e:
        return f"Error: executing Python file: {e}"

