import os

def get_files_info(working_directory, directory="."):
    try:
        # Expand ~ to user's home manually (if used)
        if working_directory.startswith("~"):
            working_directory = working_directory[1:]
        
        # Create absolute path to the requested directory
        requested_directory = os.path.join(os.path.abspath(working_directory), (directory))
        
        # Prevent directory traversal outside the working directory
        if os.path.abspath(working_directory) not in os.path.abspath(requested_directory):
            return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        
        # Validate that the path is a directory
        if os.path.isdir(requested_directory) == False:
            return(f'Error: "{directory}" is not a directory')
        
        # Get list of files/directories in the requested directory
        list_dir = os.listdir(requested_directory)
        final_string = []

        # Format the result heading based on whether it's the current directory
        if directory == ".":
            final_string.append(f"Result for current directory:")
        else:
            final_string.append(f"Result for {directory} directory:")

        # Add info for each file or directory
        for file in list_dir:
            final_string.append(
                f"- {file}: file_size={os.path.getsize(requested_directory + '/' + file)}, is_dir={os.path.isdir(requested_directory + '/' + file)}"
            )

        # Join all lines and return the final output string
        return "\n".join(final_string)
    
    except Exception as e:
        # Return error message if any standard library call fails
        return f"Error: {e}"
