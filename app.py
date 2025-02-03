import os
import json
import pandas as pd

def read_data(file_path):
    """Read data from a file based on its extension."""
    _, ext = os.path.splitext(file_path)
    
    if ext == '.csv':
        return pd.read_csv(file_path)
    elif ext == '.json':
        with open(file_path, 'r') as f:
            return json.load(f)
    elif ext == '.txt':
        with open(file_path, 'r') as f:
            return f.readlines()
    else:
        print(f"Unsupported file type: {ext}")
        return None

def display_data(data, file_name):
    """Display the data in a readable format."""
    print(f"Data from {file_name}:")
    print("---------------------")
    
    if isinstance(data, pd.DataFrame):
        print(data.to_string(index=False))  # Display DataFrame
    elif isinstance(data, dict):
        for key, value in data.items():
            print(f"{key}: {value}")
    elif isinstance(data, list):
        for item in data:
            print(f"- {item.strip()}")
    else:
        print("No data to display.")
    
    print()  # Add a newline for better readability

def main():
    input_folder = 'input_data'
    
    for file_name in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file_name)
        data = read_data(file_path)
        
        if data is not None:
            display_data(data, file_name)

if __name__ == '__main__':
    main() 