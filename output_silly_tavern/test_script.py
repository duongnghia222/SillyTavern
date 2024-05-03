file_path = '/path/to/your/file.txt'  # Replace with the actual file path

# Read the file
with open(file_path, 'r') as file:
    lines = file.readlines()

# Remove numbers from each line and keep only text
cleaned_lines = []
for line in lines:
    cleaned_line = ''.join([char for char in line if not char.isdigit()])
    cleaned_lines.append(cleaned_line)

# Print the cleaned lines
for line in cleaned_lines:
    print(line)
