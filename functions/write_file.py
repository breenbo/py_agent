import os
from functions.helpers import check_file, get_full_path


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
