import os
import shutil

def display_files():
    file_list = [file for file in os.listdir(os.path.dirname(__file__)) if os.path.isfile(os.path.join(os.path.dirname(__file__), file))]
    print("Available files:")
    for i, file in enumerate(file_list, start=1):
        print(f"{i}. {file}")

def copy_file(file_index):
    file_list = [file for file in os.listdir(os.path.dirname(__file__)) if os.path.isfile(os.path.join(os.path.dirname(__file__), file))]
    if file_index < 1 or file_index > len(file_list):
        print("Invalid selection.")
        return
    file_to_copy = file_list[file_index - 1]
    src = os.path.join(os.path.dirname(__file__), file_to_copy)
    dst = os.path.join(os.getcwd(), file_to_copy)
    shutil.copy(src, dst)
    print(f"File '{file_to_copy}' copied to current directory.")
