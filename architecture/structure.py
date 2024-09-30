import os


def print_directory_structure(
    startpath, level=2, exclude_exts=(".pyc", ".env"), exclude_dirs=("__pycache__", "pydiary.egg-info", ".venv", ".pytest_cache", ".git")
):
    """
    Prints the directory structure, excluding specific file extensions and directories.
    Parameters:
    - startpath: The root directory to start from
    - level: Maximum depth to traverse
    - exclude_exts: Tuple of file extensions to exclude (e.g., '.pyc')
    - exclude_dirs: Tuple of directory names to exclude (e.g., '__pycache__')
    """

    def tree_dir(root, depth, is_last):
        indent = ""
        if depth > 0:
            indent = "│   " * (depth - 1) + ("└── " if is_last else "├── ")
        print(f"{indent}{os.path.basename(root)}/")


    for root, dirs, files in os.walk(startpath):
        # Exclude specified directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        # Calculate depth for indentation
        depth = root.replace(startpath, "").count(os.sep)
        if depth > level:
            continue

        # Print the current directory
        tree_dir(root, depth, not dirs and not files)

        # Print files with indentation, excluding certain file extensions
        files = [f for f in files if not f.endswith(exclude_exts)]
        for i, file in enumerate(files):
            tree_file(file, depth + 1, i == len(files) - 1)

        # If there are no subdirectories, ensure directories are correctly marked
        for i, directory in enumerate(dirs):
            new_root = os.path.join(root, directory)
            print_directory_structure(new_root, level=level, exclude_exts=exclude_exts, exclude_dirs=exclude_dirs)


# Specify the correct directory path here
start_directory = r"C:\Users\Hendr\Desktop\Practice_workspace\EDiary"
print_directory_structure(start_directory)
