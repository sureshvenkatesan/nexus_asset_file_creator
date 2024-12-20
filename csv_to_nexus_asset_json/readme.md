
# CSV to JSON Converter

This repository contains a Python script [csv_to_json_convertor.py](csv_to_json_convertor.py) that converts a CSV file into a JSON file, following a specific format. The script reads the CSV file, processes each row, and generates a JSON file with the required structure.

[csv_to_json_convertor_use_slash_for_dots.py](csv_to_json_convertor_use_slash_for_dots.py) is a slight variation of the script with '/' replacing '.' in the Group field. This script is preferred over  [csv_to_json_convertor.py](csv_to_json_convertor.py) 

## Features

- Converts a CSV file to a JSON file.
- Automatically constructs the `source` path based on the fields in the CSV.
- Converts the `uploadDate` field in the CSV to a Unix timestamp for the `lastUpdated` field in the JSON.
- Designed for ease of use with command-line arguments.

## Prerequisites

- Python 3.x
- `pip install pytz`

## Installation

1. On your  local machine navigate to the project directory:

   ```bash
   cd csv-to-json-convertor
   ```

## Usage

1. Prepare your CSV file with the following columns:

   ```
   Repository, Group, Artifact, Version, file, size, uploadDate
   ```

2. Run the script with the CSV file path and the desired output JSON file path:

   ```bash
   python csv_to_json_convertor.py input.csv output.json
   or
   python csv_to_nexus_asset_json/csv_to_json_convertor_use_slash_for_dots.py input.csv output.json
   ```

### Example

Given the  CSV file [gav_assets_in_repo.csv](gav_assets_in_repo.csv)

Running the following command:

```bash
python csv_to_json_convertor.py gav_assets_in_repo.csv output_assets.json
```

Will generate the   [output_assets.json](output_assets.json) file.

Running the following command:

```bash
python csv_to_json_convertor_use_slash_for_dots.py gav_assets_in_repo.csv output_assets_use_slash_for_dots.json
```

Will generate the   [output_assets_use_slash_for_dots.json](output_assets_use_slash_for_dots.json) file.

```json
{
    "assets": [
        {
            "source": "fnv2_private_release_repository/com/example/sync/sync4_0/05e3e6f21084f2fbcefc96defe47221533c88f1e/MU5T-14H213-OAC/06917-Sync4-launch-SYNC-v1.9.0-Dev-Sign-Plusone-ALM-Leftover-107-05e3e6f210/MU5T-14H213-OAC-06917-Sync4-launch-SYNC-v1.9.0-Dev-Sign-Plusone-ALM-Leftover-107-05e3e6f210.vbf",
            "fileblobRef": "",
            "lastDownloaded": "null",
            "lastUpdated": "1699959563"
        },
        {
            "source": "fnv2_private_release_repository/com/example/sync/sync4_0/05e3e6f21084f2fbcefc96defe47221533c88f1e/MU5T-14H213-OAC/06920-Sync4-launch-SYNC-v1.9.0-Prod-Sign-Plusone-ALM-Leftover-107-05e3e6f210/MU5T-14H213-OAC-06920-Sync4-launch-SYNC-v1.9.0-Prod-Sign-Plusone-ALM-Leftover-107-05e3e6f210.vbf",
            "fileblobRef": "",
            "lastDownloaded": "null",
            "lastUpdated": "1699963989"
        }
    ]
}
```

## Arguments

- `csv_file`: Path to the input CSV file.
- `json_file`: Path to the output JSON file.

