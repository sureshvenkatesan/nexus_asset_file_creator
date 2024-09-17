import pandas as pd
import sys

def check_unique_repositories(csv_filename):
    # Read the CSV file
    df = pd.read_csv(csv_filename)
    
    # Check for unique values in the 'Repository' column
    unique_repositories = df['Repository'].unique()
    
    # Print unique repositories
    print("Unique Repositories:")
    for repo in unique_repositories:
        print(repo)

# Example usage:
# python check_repositories.py your_file.csv

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_repositories.py <csv_filename>")
    else:
        check_unique_repositories(sys.argv[1])
