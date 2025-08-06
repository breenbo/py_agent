import os
from config import FILE_READ_MAX_CHAR
from functions.helpers import check_file, get_full_path

def file_checker(full_path_abs: str, file_path: str) -> bool:
    if file_path.startswith("/"):
        print(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')

        return False

    if not os.path.isfile(full_path_abs):
        print(f'Error: File not found or is not a regular file: "{file_path}"')

        return False
    
    return True


def get_file_content(working_directory: str, file_path: str):
    is_file_valid = check_file(working_directory, file_path, file_checker)

    if not is_file_valid:
        return

    full_path_abs = get_full_path(working_directory, file_path)
    if full_path_abs == None:
        return

    print("valid file found")

    with open(full_path_abs, "r") as f:
        file_content_string = f.read(FILE_READ_MAX_CHAR)

        if len(file_content_string) < FILE_READ_MAX_CHAR:
            print(f"{file_content_string}")
        else:
            print(f'{file_content_string}[...File "{file_path}" truncated at {FILE_READ_MAX_CHAR} characters]')


        return file_content_string
