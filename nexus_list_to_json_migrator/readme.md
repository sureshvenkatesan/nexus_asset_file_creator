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

Now use the in "Nexus Migrator" tool mentioned in "Migrating from Sonatype Nexus Repository Manager to Artifactory > [Migrator Tool Overview](https://jfrog.com/help/r/jfrog-installation-setup-documentation/migrator-tool-overview)" with the the [migrateArtifact](https://jfrog.com/help/r/jfrog-installation-setup-documentation/run-the-migration-tool-in-multiple-stages) / `ma` option like:

```
./jfrog-nexus-migrator-<version>.sh ma --use-existing-asset-file="true" 
```

### Disclaimer
Your use of this code is governed by the following license:

JFrog hereby grants you a non-exclusive, non-transferable, non-distributable right to use this code solely in connection with
your use of a JFrog product or service. This code is provided 'as-is' and without any warranties or
conditions, either express or implied including, without limitation, any warranties or conditions
of title, non-infringement, merchantability or fitness for a particular cause. Nothing herein shall
convey to you any right or title in the code, other than for the limited use right set forth
herein. For the purposes hereof "you" shall mean you as an individual as well as the organization
on behalf of which you are using the software and the JFrog product or service.
