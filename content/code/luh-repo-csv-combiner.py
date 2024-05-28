import os
import csv
import argparse
import sys

def combine_csv_files(input_folder, output_file):
    """
    Combines all CSV files in the specified folder into a single CSV file.
    
    Parameters:
    input_folder (str): The path to the folder containing the CSV files.
    output_file (str): The path to the output CSV file.
    """
    print(f"Combining CSV files from folder: {input_folder} into {output_file}")
    csv.field_size_limit(sys.maxsize)
    # List to store the rows from all CSV files
    combined_rows = []
    header_saved = False
    
    # Iterate through all files in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.csv'):
            file_path = os.path.join(input_folder, file_name)
            print(f"Processing file: {file_path}")
            
            # Open and read the CSV file
            with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader)
                
                # Save header only once
                if not header_saved:
                    combined_rows.append(header)
                    header_saved = True
                
                # Add the remaining rows
                for row in reader:
                    combined_rows.append(row)
    
    # Write the combined rows to the output file
    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(combined_rows)
    
    print(f"Successfully combined CSV files into {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Combine all CSV files in a folder into a single CSV file.")
    parser.add_argument("input_folder", help="Path to the folder containing the CSV files")
    parser.add_argument("output_file", help="Path to the output combined CSV file")
    
    args = parser.parse_args()
    
    combine_csv_files(args.input_folder, args.output_file)

if __name__ == "__main__":
    main()
