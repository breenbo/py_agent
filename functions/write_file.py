import os
from functions.helpers import check_file, get_full_path
from google.genai import types

# llm function declaration
schema_write_file= types.FunctionDeclaration(
    name="write_file",
    description="Write content into a file, constrained to the working directory. If the file doesn't exists, it is created. If it already exists, it is overwritten.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file to be written, relative to the working directory.",
            ),
            "content" : types.Schema(
                type=types.Type.STRING,
                description="The content to be written into the file referenced by the file path."
            )
        },
    ),
)

def file_checker(_full_path_abs: str, file_path: str) -> bool:
    if file_path.startswith("/"):
        print(f'Error: Cannot write "{file_path}" as it is outside the permitted working directory')

        return False
   
    return True


def write_file(working_directory: str, file_path: str, content: str):
    is_file_valid = check_file(working_directory, file_path, file_checker)

    if not is_file_valid:
        return

    full_path_abs = get_full_path(working_directory, file_path)
    if full_path_abs == None:
        return

    try:
        if not os.path.exists(full_path_abs):
            dirs_path = "/".join(full_path_abs.split("/")[:-1])
            os.makedirs(dirs_path, exist_ok=True)

        with open(full_path_abs, "w") as f:
            chars_written = f.write(content)
            print(f'Successfully wrote to "{file_path}" ({chars_written} characters written)')

    except Exception as e:
        print(f"Error: {e}")
