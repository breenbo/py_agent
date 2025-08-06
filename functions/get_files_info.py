import os

def get_full_path(working_directory: str, directory: str):
    try:
        full_path = os.path.join(working_directory, directory)
        full_path_abs = os.path.abspath(full_path)
        return full_path_abs
    except Exception as e:
        print(f"Error: {e}")


def get_files_info(working_directory: str, directory: str = "."):
    if directory.startswith("/"):
        print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        return


    full_path_abs= get_full_path(working_directory, directory)
    if full_path_abs == None:
        return

    wd_directories = full_path_abs.split("/")

    if working_directory not in wd_directories:
        print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        return

    if not os.path.isdir(full_path_abs):
        print(f'Error: "{directory}" is not a directory')
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

