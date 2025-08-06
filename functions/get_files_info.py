import os
from functions.helpers import get_full_path, check_file
from google.genai import types

# llm function declaration
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def dir_checker(full_path_abs: str, file_path: str):
    if file_path.startswith("/"):
        print(f'Error: Cannot list "{file_path}" as it is outside the permitted working directory')
        return False

    if not os.path.isdir(full_path_abs):
        print(f'Error: "{file_path}" is not a directory')
        return False

    return True



def get_files_info(working_directory: str, directory: str = "."):

    is_directory_valid = check_file(working_directory, directory, dir_checker)

    if not is_directory_valid: 
        return

    full_path_abs= get_full_path(working_directory, directory)
    if full_path_abs == None:
        return


    # display title
    if directory == ".":
        print("Result for current directory:")
    else:
        print(f"Result for '{directory}' directory:")

    # display dir infos
    directories = os.listdir(full_path_abs)

    for dir in directories:
        if not dir.startswith("__"):
            try:
                abs_path= os.path.join(full_path_abs, dir)
                file_size= os.path.getsize(abs_path)
                is_dir= os.path.isdir(abs_path)

                print(f" - {dir}: file_size={file_size} bytes, is_dir={is_dir}")
            except Exception as e:
                print(f"Error: {e}")

