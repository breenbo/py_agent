import os, sys
import subprocess
from functions.helpers import Action, check_file, get_full_path

def file_checker(full_path_abs: str, file_path: str):
    if file_path.startswith("/"):
        print(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')

        return False

    if not os.path.isfile(full_path_abs):
        print(f'Error: File "{file_path}" not found.')

        return False

    if not file_path.endswith(".py"):
        print(f'Error: "{file_path}" is not a Python file.')

        return False

    return True


def run_python_file(working_directory: str, file_path: str, args: list[str] = []):
    is_file_valid = check_file(working_directory, file_path, file_checker, Action.execute)

    if not is_file_valid:
        print("STDOUT:")
        return

    full_path = get_full_path(working_directory, file_path)
    if not full_path:
        return

    try:
        cmd = ["python3", full_path] + args
        result = subprocess.run(cmd, capture_output=True, text=True)

        result_str = f"STDOUT: {result.stdout}"

        if result.stderr != "":
            result_str += f"STDERR: {result.stderr}"
        if result.returncode != 0:
            result_str += f"Process excited with code {result.returncode}"

        if result.stdout == "" and result.stderr == "":
            result_str = "No output produced"

        return result_str
    except Exception as e:
        return f"Error: executing Python file: {e}"
