# CSV Reformatting Tool

A Python script to reformat a CSV file by rearranging columns and modifying specific fields, particularly removing `.zip` from the `file` field.


## Features
- Rearranges columns: `Repository`, `Group`, `Artifact`, `Version`, `file`, `size`, `uploadDate`
- Flexible input and output paths via command-line arguments

## Input Format

The input CSV file must have the following columns:
- `Artifact`
- `Version`
- `Group`
- `Repository`
- `file`
- `url`
- `size`
- `uploadDate`

### Example Input

```csv
Artifact,Version,Group,Repository,file,url,size,uploadDate
ECG2-milestone-2023-11-VMCU-Production-Sign,0.0.50.378,com.example.ecg2.ECG2-milestone-2023-11-VMCU-Production-Sign,fnv2_private_release_repository,ECG2-milestone-2023-11-VMCU-Production-Sign-0.0.50.378.zip,https://www.nexus.example.com/repository/fnv2_private_release_repository/com/example/ecg2/ECG2-milestone-2023-11-VMCU-Production-Sign/ECG2-milestone-2023-11-VMCU-Production-Sign/0.0.50.378/ECG2-milestone-2023-11-VMCU-Production-Sign-0.0.50.378.zip,4088355,"Fri, 05 Jan 2024 20:29:04 GMT"

## Output Format

The output CSV file will have the following columns:

- `Repository`
- `Group`
- `Artifact`
- `Version`
- `file`
- `size`
- `uploadDate`

### Example Output

```csv
Repository,Group,Artifact,Version,file,size,uploadDate
fnv2_private_release_repository,com.example.ecg2.ECG2-milestone-2023-11-VMCU-Production-Sign,ECG2-milestone-2023-11-VMCU-Production-Sign,0.0.50.378,ECG2-milestone-2023-11-VMCU-Production-Sign-0.0.50.378.zip,4088355,"Fri, 05 Jan 2024 20:29:04 GMT"

## How to Use

Run the script from the command line using the following format:

```bash
python csv2format_to_correct_csv_format.py <input_csv>  <output_csv>
```
