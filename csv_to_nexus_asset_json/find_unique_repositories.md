
# Find Unique Repositories in CSV

This [find_unique_repositories.py](find_unique_repositories.py) Python script reads a CSV file and prints the unique values in the `Repository` column. The script takes the CSV filename as a command-line argument.

## Prerequisites

Make sure you have Python installed on your system along with the `pandas` library. You can install `pandas` using `pip` if you don't have it already:

```bash
pip install pandas
```

## Usage

1. Clone this repository or download the script `find_unique_repositories.py`.

2. Run the script with your CSV file as an argument.

```bash
python find_unique_repositories.py <csv_filename>
```

### Example:

If you have a CSV file named `artifacts.csv`, you would run the following command:

```bash
python find_unique_repositories.py artifacts.csv
```

The script will output the unique values in the `Repository` column of the CSV file.

### Sample Output:

```
Unique Repositories:
fnv2_private_release_repository
another_repository_name
...
```

## File Format

The CSV file should have the following format:

```csv
Repository,Group,Artifact,Version,file,size,uploadDate
fnv2_private_release_repository,com.example.sync,artifact1,version1,file1,12345,uploadDate1
fnv2_private_release_repository,com.example.sync,artifact2,version2,file2,67890,uploadDate2
```

Make sure the column `Repository` exists in your CSV file for the script to work correctly.
