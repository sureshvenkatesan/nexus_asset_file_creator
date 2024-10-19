import csv
import argparse

# Function to process the CSV and reformat it
def reformat_csv(input_file, output_file):
    # Open the input CSV file
    with open(input_file, mode='r') as infile:
        reader = csv.DictReader(infile)
        # Define the column names for the output CSV
        fieldnames = ['Repository', 'Group', 'Artifact', 'Version', 'file', 'size', 'uploadDate']
        
        # Open the output CSV file
        with open(output_file, mode='w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Iterate over the rows in the input CSV
            for row in reader:
                # Extract required fields and restructure the data
                reformatted_row = {
                    'Repository': row['Repository'],
                    'Group': row['Group'],
                    'Artifact': row['Artifact'],
                    'Version': row['Version'],
                    #'file': row['file'].replace(".zip", ""),  # Modify file field as needed
                    'file': row['file'],
                    'size': row['size'],
                    'uploadDate': row['uploadDate']
                }
                writer.writerow(reformatted_row)

# Setup argparse for input and output files
def main():
    parser = argparse.ArgumentParser(description='Reformat CSV file.')
    parser.add_argument('input_file', help='Path to the input CSV file.')
    parser.add_argument('output_file', help='Path to the output CSV file.')
    
    args = parser.parse_args()
    
    reformat_csv(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
