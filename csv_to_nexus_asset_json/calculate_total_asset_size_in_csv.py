import pandas as pd
import argparse

# Function to convert bytes to human-readable format
def convert_size(bytes_size):
    for unit in ['Bytes', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024

# Function to process the CSV file and calculate the total size
def calculate_total_size(file_path, start_line=None, end_line=None):
    # Load CSV into DataFrame
    df = pd.read_csv(file_path)

    # Convert size column to numeric
    df['size'] = pd.to_numeric(df['size'])

    # If start and end lines are provided, slice the DataFrame
    if start_line is not None and end_line is not None:
        df = df.iloc[start_line-1:end_line]

    # Sum the size column
    total_size_bytes = df['size'].sum()

    # Convert and print the total size in human-readable format
    total_size_human_readable = convert_size(total_size_bytes)
    print(f"Total size: {total_size_human_readable}")

# Set up argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate total size from CSV file with optional line range")
    parser.add_argument("csv_file", help="Path to the CSV file")
    parser.add_argument("--start", type=int, help="Start line number (optional)", default=None)
    parser.add_argument("--end", type=int, help="End line number (optional)", default=None)
    args = parser.parse_args()

    # Calculate total size
    calculate_total_size(args.csv_file, args.start, args.end)
