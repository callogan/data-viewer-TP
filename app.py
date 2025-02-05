import os
import pandas as pd
import saspy
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize SAS session
sas = saspy.SASsession()

def read_data(file_path):
    """Read data from a file based on its extension."""
    _, ext = os.path.splitext(file_path)
    logging.info(f"Attempting to read file: {file_path} with extension: {ext}")
    
    if ext == '.csv':
        try:
            data = pd.read_csv(file_path)
            logging.info(f"Successfully read CSV file: {file_path}")
            return data
        except Exception as e:
            logging.error(f"Error reading CSV file {file_path}: {e}")
            return None
    elif ext == '.xlsx':
        try:
            # Read all sheets into a dictionary of DataFrames
            xls = pd.ExcelFile(file_path)
            data = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}
            logging.info(f"Successfully read Excel file: {file_path} with sheets: {list(data.keys())}")
            return data
        except Exception as e:
            logging.error(f"Error reading Excel file {file_path}: {e}")
            return None
    elif ext in ['.sas7bdat', '.xpt', '.cpt']:
        try:
            # Use saspy to read SAS files
            data = sas.sasdata(file_path).to_data_frame()
            logging.info(f"Successfully read SAS file: {file_path}")
            return data
        except Exception as e:
            logging.error(f"Error reading SAS file {file_path}: {e}")
            return None
    else:
        logging.warning(f"Unsupported file type: {ext} for file: {file_path}")
        return None

def display_data(data, file_name):
    """Display the data in a readable format."""
    logging.info(f"Displaying data from file: {file_name}")
    print(f"Data from {file_name}:")
    print("---------------------")
    
    if isinstance(data, dict):  # For Excel files with multiple sheets
        for sheet_name, df in data.items():
            print(f"Sheet: {sheet_name}")
            print(df.to_string(index=False))  # Display DataFrame
            print()  # Add a newline for better readability
    elif isinstance(data, pd.DataFrame):
        print(data.to_string(index=False))  # Display DataFrame
    else:
        logging.warning("No data to display.")
        print("No data to display.")
    
    print()  # Add a newline for better readability

def main():
    input_folder = 'input_data'
    logging.info(f"Starting data processing in folder: {input_folder}")
    
    for file_name in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file_name)
        logging.info(f"Processing file: {file_path}")
        data = read_data(file_path)
        
        if data is not None:
            display_data(data, file_name)
        else:
            logging.warning(f"No data returned for file: {file_path}")

if __name__ == '__main__':
    main() 