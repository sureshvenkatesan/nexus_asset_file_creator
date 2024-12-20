# Nexus Repository Asset Comparison Tool

[compare_nexus_repo_asset_to_jpd_repo.py](compare_nexus_repo_asset_to_jpd_repo.py) Python script compares repository assets between a Nexus asset map and an Artifactory repo list json file to identify mismatches in SHA1 hashes and file paths.

## Prerequisites

- Python 3.x
- JSON input files:
  - Artifactory repo artifact list JSON file (e.g., `corp_releases_east.json`) referred to as the `--east-json` file
  - Asset map JSON file (e.g., `corp_releases_assetmap.json`) from Nexus

Note: Sample input json files are in [input](input) and output files are in the [output](output).

## Usage
```bash
python compare_nexus_repo_asset_to_jpd_repo.py \
--east-json <path_to_east_json> \
--assetmap-json <path_to_assetmap_json> \
--repo-name <repository_name>
```
### Arguments

- `--east-json`: Path to the East JSON file
- `--assetmap-json`: Path to the asset map JSON file
- `--repo-name`: Repository name (e.g., corp_releases) . Assuming using same repo name in both Nexus and Artifactory

## Input File Formats

### East JSON Format
```json
{
  "uri": "https://...",
  "created": "2024-12-20T05:47:55.088Z",
  "files": [
    {
      "uri": "/path/to/file",
      "sha1": "ef19e97d1c5b317a22b134b61f9bc53d38982f3b",
      ...
    }
  ]
}
```

### Asset Map JSON Format
```json
{
  "assets": [
    {
      "source": "repo_name/path/to/file",
      "nexusAssetSha1": "2b0aabfe52a8e1ed3b7ad1919102b397360cdefa",
      ...
    }
  ]
}
```

### Example

```bash
python compare_nexus_repo_asset_to_jpd_repo.py \
    --east-json corp_releases_east.json \
    --assetmap-json corp_releases_assetmap.json \
    --repo-name corp_releases
```

## Output Files

The script generates three output files:

1. `nexusAssetSha1_not_in_<repo_name>_east.json`
   - Contains assets whose SHA1 values in the asset map don't exist in the East JSON file
   - Output follows the same JSON format as the input asset map

2. `nexus_source_not_in_<repo_name>_east.json`
   - Contains assets that either:
     - Exist in both files but have different SHA1 values
     - Exist in the Nexus asset map but are missing from the East JSON file
   - Output follows the same JSON format as the input asset map

3. `<repo_name>_assetmap_delta.json`
   - Contains a combined list of all mismatched assets from both above files
   - Includes both SHA1 mismatches and source mismatches without duplicates
   - Output follows the same JSON format as the input asset map

### Output File Format
```json
{
  "assets": [
    {
      "source": "repo_name/path/to/file",
      "nexusAssetSha1": "2b0aabfe52a8e1ed3b7ad1919102b397360cdefa",
      ...
    }
  ]
}
```



## Error Handling

- The script will raise an error if any of the required input files are not found
- The script will raise an error if the JSON files are not properly formatted
- All arguments are required; the script will show a help message if any are missing

