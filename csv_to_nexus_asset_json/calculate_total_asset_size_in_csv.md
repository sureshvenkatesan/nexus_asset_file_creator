# Calculate Total Asset Size in CSV

[csv_to_nexus_asset_json/calculate_total_asset_size_in_csv.py](csv_to_nexus_asset_json/calculate_total_asset_size_in_csv.py) Python script reads a CSV file containing data with a `size` column (in bytes) and calculates the total size of assets. It also allows users to optionally specify the start and end line numbers to calculate the size only for a specific range of lines.

## Features
- Reads a CSV file with a `size` column in bytes.
- Sums the values in the `size` column.
- Converts the total size into a human-readable format (Bytes, KB, MB, GB, or TB).
- Optionally calculates the total size for a specific range of lines.
- If no range is provided, it calculates the total asset size for the entire file.

## Prerequisites

- Python 3.x
- Pandas library

You can install pandas using the following command:

```bash
pip install pandas
```

## Usage

To use this script, follow these steps:

1. Save the script as `calculate_total_asset_size_in_csv.py`.
2. Open your terminal.
3. Run the script with the path to your CSV file as a command-line argument.

### Example command:

```bash
python calculate_total_asset_size_in_csv.py your_file.csv
```

### Optional Arguments:

- `--start`: The start line number (optional).
- `--end`: The end line number (optional).

### Examples:

1. **Calculate the total size for the entire file:**
   ```bash
   python calculate_total_asset_size_in_csv.py your_file.csv
   ```

2. **Calculate the total size for lines 2 to 10:**
   ```bash
   python calculate_total_asset_size_in_csv.py your_file.csv --start 2 --end 10
   ```

### CSV File Format

The script expects the CSV file to have a column named `size` where the sizes are expressed in bytes. Here is a sample of how the CSV file should look:

```
Repository,Group,Artifact,Version,file,size,uploadDate
repo1,com.example,artifact1,1.0.0,artifact1.vbf,12345678,"Tue, 14 Nov 2023 02:59:23 GMT"
repo2,com.example,artifact2,1.0.1,artifact2.vbf,87654321,"Tue, 14 Nov 2023 04:13:09 GMT"
```

### Output

The script will print the total size of assets in a human-readable format. For example:

```
Total size: 92.97 MB
```

## Arguments

- `csv_file`: The path to the CSV file containing the size data.
- `--start`: (Optional) The starting line number to include in the calculation.
- `--end`: (Optional) The ending line number to include in the calculation.

## Example Output

```bash
python calculate_total_asset_size_in_csv.py assets.csv
Total size: 75.65 MB
```

```bash
python calculate_total_asset_size_in_csv.py assets.csv --start 2 --end 10
Total size: 50.12 MB
```
