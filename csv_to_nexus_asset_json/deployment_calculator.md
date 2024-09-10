
# Deployment Calculator

[deployment_calculator.py](deployment_calculator.py) is a Python script that calculates the speed of deployment (artifacts per minute) and estimates the time remaining for a full deployment based on historical data. It takes the number of artifacts deployed, the start and end timestamps, and provides an estimated completion time.

## Features

- Calculates deployment speed in artifacts per minute.
- Estimates the remaining time to complete the deployment in days.

## Requirements

- Python 3.x

## Usage

To use the script, pass the required parameters: the number of initial and final deployed artifacts, the total number of artifacts to be deployed, and the start and end times in a specific format.

### Example Command

```bash
python deployment_calculator.py --initial_artifacts 11511 --final_artifacts 32449 --total_artifacts 136814 --start_time "Sep 5, 10:17:48 AM" --end_time "Sep 9, 11:04:43 PM"
```

### Parameters

- `--initial_artifacts` : Number of artifacts that had been deployed at the start time.
- `--final_artifacts` : Number of artifacts deployed by the end time.
- `--total_artifacts` : Total number of artifacts to be deployed.
- `--start_time` : Start timestamp in the format `Sep 5, 10:17:48 AM`.
- `--end_time` : End timestamp in the format `Sep 9, 11:04:43 PM`.

### Example Output

```bash
The deployment speed is approximately 3.21 artifacts per minute.
Based on this speed, the deployment is estimated to be completed in approximately 22.59 days.
```



## Running the Script


Once in the script directory, run the script using:

```bash
python deployment_calculator.py --initial_artifacts <initial> --final_artifacts <final> --total_artifacts <total> --start_time "<start_time>" --end_time "<end_time>"
```

Replace the parameters with your actual data.

