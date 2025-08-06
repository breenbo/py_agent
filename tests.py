from functions.run_python_file import run_python_file
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file


# get_files_info("calculator", ".")
# get_files_info("calculator", "pkg")
# get_files_info("calculator", "../")
# get_files_info("calculator", "/bin")
#
# _ = get_file_content("calculator", "main.py")
# _ = get_file_content("calculator", "pkg/calculator.py")
# _ = get_file_content("calculator", "/bin/cat")
# _ = get_file_content("calculator", "pkg/does_not_exist.py")

# write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
# write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
# write_file("calculator", "/tmp/temp.txt", "this should not be allowed")

_=run_python_file("calculator", "main.py")
_=run_python_file("calculator", "main.py", ["3 + 5"])
_=run_python_file("calculator", "tests.py")
_=run_python_file("calculator", "../main.py")
_=run_python_file("calculator", "nonexistent.py")
