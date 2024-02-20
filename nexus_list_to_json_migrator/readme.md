# Nexus List to JSON Migrator

## Description
This script migrates data from a Nexus list CSV file to JSON format. It parses the input CSV file, organizes the data into repositories, and generates separate JSON files for each repository's assets.

## Prerequisites
- Python 3.x


## Usage
1. Ensure you have Python 3.x installed on your system.

2. Run the script with the following command:
    ```
    python nexus_list_to_json_migrator.py --input-file <path_to_input_file> --output-path <output_directory>
    ```
    - `--input-file`: Path to the input CSV file containing the data.
    - `--output-path`: Directory where the output JSON files will be saved. If not provided, it will default to `/Users/angellom/Downloads/atnt/test_json`.

## Example
```
python nexus_list_to_json_migrator.py --input-file /path/to/maven_artifacts.csv --output-path /path/to/output_directory
```

## Input CSV Format
The input CSV file should contain lines with the following format:
```
<repository_name>,<path_to_asset>
```
For example:
```
repo1,/path/to/asset1
repo2,/path/to/asset2
```

## Output
The script generates JSON files named `<repository_name>_assetmap.json` for each repository found in the input CSV file. These files contain information about the assets associated with each repository.
