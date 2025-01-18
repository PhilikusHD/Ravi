import os
import shutil

# List of files and directories to remove
files_to_remove = [
    ".ninja_deps",
    ".ninja_log",
    "build.ninja",
    "cmake_install.cmake",
    "CMakeCache.txt",
    "obj/",
    "Intermediates"
]

# Function to remove files
def remove_files(root_path, filenames):
    for root, dirs, files in os.walk(root_path):
        for name in filenames:
            path = os.path.join(root, name)
            if os.path.exists(path):
                try:
                    if os.path.isfile(path):
                        os.remove(path)
                    elif os.path.isdir(path):
                        continue
                except OSError as e:
                    print(f"Error while removing {path}: {e.strerror}")

# Function to remove directories
def remove_directories(root_path, directory_name):
    for root, dirs, files in os.walk(root_path):
        for dir_name in dirs:
            if dir_name == directory_name:
                path = os.path.join(root, dir_name)
                if os.path.exists(path):
                    try:
                        shutil.rmtree(path)
                        #print("Removed directory:", path)
                    except OSError as e:
                        print(f"Error while removing {path}: {e.strerror}")


def Clean(type, build_dir=None):
    root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    build_dir = build_dir or root_directory

    if type == "build":
        # Remove files
        remove_files(root_directory, files_to_remove)
        remove_files(build_dir, files_to_remove)

        # Remove CMakeFiles and Output directories
        remove_directories(root_directory, "CMakeFiles")
        remove_directories(root_directory, "Output")
        remove_directories(build_dir, "CMakeFiles")

    elif type == "all":
        # Remove files and directories
        remove_files(root_directory, files_to_remove)

        # Remove additional directories for a full clean
        remove_directories(root_directory, "CMakeFiles")
        remove_directories(root_directory, "Output")
        remove_directories(root_directory, "bin")
        remove_directories(root_directory, "obj")
        remove_directories(root_directory, "lib")

        if build_dir != root_directory and os.path.exists(build_dir):
            shutil.rmtree(build_dir)