import os
from typing import Callable

def get_full_path(working_directory: str, path: str):
    try:
        full_path = os.path.join(working_directory, path)
        full_path_abs = os.path.abspath(full_path)
        return full_path_abs
    except Exception as e:
        print(f"Error: {e}")



def check_file(working_directory: str, file_path: str, checker: Callable[[str, str], bool]):
    full_path_abs= get_full_path(working_directory, file_path)
    if full_path_abs == None:
        return False

    wd_directories = full_path_abs.split("/")

    if working_directory not in wd_directories:
        print(f'Error: Cannot list "{file_path}" as it is outside the permitted working directory')
        return False

    is_ok = checker(full_path_abs, file_path)

    return is_ok


