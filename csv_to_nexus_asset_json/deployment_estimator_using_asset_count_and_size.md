# Deployment Estimator Using Asset Count and Size

The [deployment_estimator_using_asset_count_and_size.py](deployment_estimator_using_asset_count_and_size.py) script calculates the deployment speed based on the number of artifacts and their sizes. It estimates the time remaining for the deployment and provides the estimated completion date.

## Features
- **Deployment Speed Calculation**: Calculates deployment speed based on the number of artifacts migrated and their total size.
- **Estimated Completion Time**: Provides the estimated time left for the deployment to complete in days, hours, minutes, and seconds.
- **Flexible Time Calculation**: Allows using the current time or the provided end time as the base for calculating the estimated completion date.
- **Human-Readable Size Conversion**: Converts artifact sizes from bytes to a human-readable format (KB, MB, GB, etc.).

## Requirements
- Python 3.9+
- `pandas` library
- `zoneinfo` (for Python < 3.9, use `pytz`)

Install the required library with:
```bash
pip install pandas
```

## Usage
```bash
python deployment_estimator_using_asset_count_and_size.py --csv_file <CSV_FILE> \
                                                          --initial_artifacts <INITIAL_ARTIFACT_LINE> \
                                                          --final_artifacts <FINAL_ARTIFACT_LINE> \
                                                          --total_artifacts <TOTAL_ARTIFACT_LINE> \
                                                          --start_time "<START_TIME>" \
                                                          --end_time "<END_TIME>" \
                                                          [--use_end_time_for_completion]
```

### Arguments:
- `--csv_file`: Path to the CSV file containing artifact details.
- `--initial_artifacts`: Line number in the CSV file corresponding to the artifact when the deployment started.
- `--final_artifacts`: Line number in the CSV file corresponding to the artifact currently being migrated.
- `--total_artifacts`: Line number in the CSV file corresponding to the final artifact to be migrated.
- `--start_time`: Start time of the deployment in the format: `"Sep 9, 2024, 9:04:43 PM"`.
- `--end_time`: End time (current or recent time) in the same format as `--start_time`.
- `--use_end_time_for_completion`: Use the provided `--end_time` as the base for estimated completion time calculation instead of the current UTC time.

### Example:
```bash
python deployment_estimator_using_asset_count_and_size.py --csv_file artifacts.csv \
                                                          --initial_artifacts 100 \
                                                          --final_artifacts 500 \
                                                          --total_artifacts 1000 \
                                                          --start_time "Sep 9, 2024, 9:04:43 PM" \
                                                          --end_time "Sep 17, 2024, 3:09:58 PM" \
                                                          --use_end_time_for_completion
```

### Output:
- The script will output:
  - Number of pending artifacts.
  - Total size of pending artifacts (in a human-readable format).
  - Deployment speed (artifacts/second and size/second).
  - Estimated time left for the deployment to complete (in days, hours, minutes, and seconds).
  - Estimated completion date and time.

Sample Output:
```
Pending artifacts: 65005
Total size of pending artifacts: 95.80 TB
Deployment speed: 0.04 artifacts/second or 78.76 MB /second
Deployment speed: 2.60 artifacts/minute or 4.62 GB /minute
Based on this speed, the deployment is estimated to be completed in approximately 17 days, 8 hours, 35 minutes, and 46 seconds.
The actual estimated completion date is: Oct 07, 2024, 01:46:32 AM PDT
```