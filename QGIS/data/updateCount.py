# updateCount.py

import os

# Define the file path
file_path = 'updateCount.txt'

# Check if the file exists and read the current count
if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if lines:
            last_number = int(lines[-1].strip())
        else:
            last_number = 0
else:
    last_number = 0

# Increment the count
new_number = last_number + 1

# Append the new number to the file
with open(file_path, 'a') as file:
    file.write(f"{new_number}\n")

print(f"Updated count to {new_number}")

