import pandas as pd
import argparse
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # Use pytz for Python < 3.9

# Function to parse the CSV and return relevant columns
def load_csv(filename):
    df = pd.read_csv(filename)
    df['size'] = df['size'].astype(int)  # Ensure the 'size' column is used and converted to integers
    return df

# Function to convert bytes to human-readable format
def convert_size(bytes_size):
    for unit in ['Bytes', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024

# Function to calculate deployment speed and estimate completion time
# Function to calculate deployment speed and estimate completion time
def calculate_deployment_speed(df, initial_artifact_line, final_artifact_line, total_artifacts_line, start_time, end_time, use_end_time_for_completion):
    # Get the initial, final, and total artifact data based on line numbers
    initial_artifacts = df.iloc[:initial_artifact_line]
    final_artifacts = df.iloc[:final_artifact_line]
    total_artifacts = df.iloc[:total_artifacts_line]

    # Calculate the number of artifacts and total size in bytes
    initial_size = initial_artifacts['size'].sum()
    final_size = final_artifacts['size'].sum()
    total_size = total_artifacts['size'].sum()

    pending_artifacts = total_artifacts_line - final_artifact_line
    pending_size = total_size - final_size

    # Get the user's system local timezone
    local_tz = datetime.now().astimezone().tzinfo

    # Calculate the time elapsed in seconds, converting user-provided time to UTC
    time_format = '%b %d, %Y, %I:%M:%S %p'  # Include the year, month, day, time, and AM/PM
    start_time_dt = datetime.strptime(start_time, time_format).replace(tzinfo=local_tz)
    end_time_dt = datetime.strptime(end_time, time_format).replace(tzinfo=local_tz)
    
    # Convert times to UTC for calculation
    start_time_utc = start_time_dt.astimezone(ZoneInfo('UTC'))
    end_time_utc = end_time_dt.astimezone(ZoneInfo('UTC'))

    time_elapsed = (end_time_utc - start_time_utc).total_seconds()

    # Calculate speed (artifacts and bytes per second)
    migrated_artifacts = final_artifact_line - initial_artifact_line
    migrated_size = final_size - initial_size
    speed_per_artifact_sec = migrated_artifacts / time_elapsed if migrated_artifacts > 0 else 0
    speed_per_size_sec = migrated_size / time_elapsed if migrated_size > 0 else 0

    # Calculate speed per minute
    speed_per_artifact_min = speed_per_artifact_sec * 60
    speed_per_size_min = speed_per_size_sec * 60

    print(f"Pending artifacts: {pending_artifacts}")
    print(f"Total size of pending artifacts: {convert_size(pending_size)}")
    print(f"Deployment speed: {speed_per_artifact_sec:.2f} artifacts/second or {convert_size(speed_per_size_sec)} /second")
    print(f"Deployment speed: {speed_per_artifact_min:.2f} artifacts/minute or {convert_size(speed_per_size_min)} /minute")

    # Estimate remaining deployment time (seconds)
    if speed_per_artifact_sec > 0 or speed_per_size_sec > 0:
        remaining_time_artifacts = pending_artifacts / speed_per_artifact_sec if speed_per_artifact_sec > 0 else float('inf')
        remaining_time_size = pending_size / speed_per_size_sec if speed_per_size_sec > 0 else float('inf')

        # Take the max of both times for the estimate
        estimated_completion_time = max(remaining_time_artifacts, remaining_time_size)
        days, rem = divmod(estimated_completion_time, 86400)  # seconds in a day
        hours, rem = divmod(rem, 3600)  # seconds in an hour
        minutes, seconds = divmod(rem, 60)

        # Choose either current UTC time or --end_time as the base for calculation
        if use_end_time_for_completion:
            completion_base_time = end_time_utc  # Use the provided --end_time in UTC
        else:
            completion_base_time = datetime.now().astimezone(ZoneInfo('UTC'))  # Use current UTC time

        estimated_completion_date = completion_base_time + timedelta(seconds=estimated_completion_time)

        # Convert the estimated completion time back to the user's local timezone
        estimated_completion_date_local = estimated_completion_date.astimezone(local_tz)

        print(f"Based on this speed, the deployment is estimated to be completed in approximately {int(days)} days, {int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds.")
        print(f"The actual estimated completion date is: {estimated_completion_date_local.strftime('%b %d, %Y, %I:%M:%S %p %Z')}")
    else:
        print("No artifacts pending deployment or migration speed is too slow to estimate.")


def main():
    parser = argparse.ArgumentParser(description="Calculate deployment speed based on artifacts and size.")
    parser.add_argument('--csv_file', required=True, help='CSV file with artifact list')
    parser.add_argument('--initial_artifacts', type=int, required=True, help='Line number for initial artifact')
    parser.add_argument('--final_artifacts', type=int, required=True, help='Line number for final artifact currently migrating')
    parser.add_argument('--total_artifacts', type=int, required=True, help='Line number for the total number of artifacts to migrate')
    parser.add_argument('--start_time', required=True, help='Start time in format: "Sep 9, 2024, 9:04:43 PM"')
    parser.add_argument('--end_time', required=True, help='End time in format: "Sep 17, 2024,  3:09:58 PM"')
    parser.add_argument('--use_end_time_for_completion', action='store_true', help='Use end_time for estimated completion calculation instead of current UTC time')

    args = parser.parse_args()

    # Load artifacts from CSV
    df = load_csv(args.csv_file)

    # Calculate deployment speed and estimated completion time
    calculate_deployment_speed(df, args.initial_artifacts, args.final_artifacts, args.total_artifacts, args.start_time, args.end_time, args.use_end_time_for_completion)

if __name__ == '__main__':
    main()
