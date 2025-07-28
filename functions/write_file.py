import os
def write_file(working_directory, file_path, content):
    try:
        # file path of the file that will be written to or overwritten 
        file_to_write = os.path.join(os.path.abspath(working_directory), file_path)

        # Prevent directory traversal outside working directory
        if os.path.abspath(working_directory) not in os.path.abspath(file_to_write):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        

        # Remove file name and extension for directory check below
        path_without_file = file_to_write.split("/")
        path_without_file = path_without_file[0:len(path_without_file) - 1 ]
        path_without_file = "/".join(path_without_file)

        # Check if the directory path exists, if not, make it
        if os.path.exists(os.path.abspath(path_without_file)) == False:
            
            os.makedirs(os.path.abspath(path_without_file))
        
        # Write contents to file
        with open(os.path.abspath(file_to_write), "w") as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    # Return error message if any standard library call fails
    except Exception as e:
        return f"Error: {e}"
