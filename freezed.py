import os
import sys


def gather_freezed_files_info(directory):
    freezed_files = []
    cubit_files = []
    aem_files = []
    total_lines_freezed = 0
    total_lines_cubit = 0
    total_lines_aem = 0

    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".freezed.dart"):
                file_path = os.path.join(root, file)
                freezed_files.append(file_path)

                # Count the number of lines in the file
                with open(file_path, "r") as f:
                    lines = f.readlines()
                    total_lines_freezed += len(lines)

                    # Check if the file is a cubit or aem file
                    if "cubit" in file:
                        cubit_files.append(file_path)
                        total_lines_cubit += len(lines)
                    elif "aem" in file:
                        aem_files.append(file_path)
                        total_lines_aem += len(lines)

    return (
        len(freezed_files),
        total_lines_freezed,
        len(cubit_files),
        total_lines_cubit,
        len(aem_files),
        total_lines_aem,
    )


# Specify the directory to search
if len(sys.argv) != 2:
    print("Usage: python freezed.py <directory>")
    sys.exit(1)

directory = sys.argv[1]

# Get the total number of freezed files and total lines of code
(
    total_files_freezed,
    total_lines_freezed,
    total_files_cubit,
    total_lines_cubit,
    total_files_aem,
    total_lines_aem,
) = gather_freezed_files_info(directory)

print(f"Total number of .freezed.dart files: {total_files_freezed}")
print(f"Total number of lines of code in .freezed.dart files: {total_lines_freezed}")
print(f"Total number of cubit files: {total_files_cubit}")
print(f"Total number of lines of code in cubit files: {total_lines_cubit}")
print(f"Total number of aem files: {total_files_aem}")
print(f"Total number of lines of code in aem files: {total_lines_aem}")
