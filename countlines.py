import os

def count_lines_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return sum(1 for line in file)
    except UnicodeDecodeError:
        print(f"Skipping non-text file: {file_path}")
        return 0

def count_lines_in_folder(folder_path):
    total_lines = 0
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            lines_in_file = count_lines_in_file(file_path)
            total_lines += lines_in_file
            print(f"File: {file_path}, Lines: {lines_in_file}")
    return total_lines


folder_path = "/Users/vijayasais/Documents/Office/Personal/Work/HarvestHub/"
total_lines = count_lines_in_folder(folder_path)
print(f"Total lines in all files: {total_lines}")
