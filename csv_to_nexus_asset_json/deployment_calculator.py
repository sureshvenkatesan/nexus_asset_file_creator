import argparse
from datetime import datetime

# Function to calculate deployment speed and estimated time
def calculate_deployment_speed(initial_artifacts, final_artifacts, total_artifacts, start_time, end_time):
    # Convert the time strings to datetime objects
    start_dt = datetime.strptime(start_time, "%b %d, %I:%M:%S %p")
    end_dt = datetime.strptime(end_time, "%b %d, %I:%M:%S %p")
    
    # Calculate the time difference in minutes
    time_difference_minutes = (end_dt - start_dt).total_seconds() / 60
    
    # Calculate the number of artifacts deployed
    artifacts_deployed = final_artifacts - initial_artifacts
    
    # Calculate the deployment speed (artifacts per minute)
    deployment_speed = artifacts_deployed / time_difference_minutes
    
    # Calculate the remaining artifacts to be deployed
    remaining_artifacts = total_artifacts - final_artifacts
    
    # Calculate the estimated time to complete the deployment (in minutes)
    estimated_minutes_remaining = remaining_artifacts / deployment_speed
    
    # Convert the estimated time from minutes to days
    estimated_days_remaining = estimated_minutes_remaining / (24 * 60)
    
    return deployment_speed, estimated_days_remaining

# Set up argument parser
parser = argparse.ArgumentParser(description="Calculate deployment speed and estimate completion time.")
parser.add_argument('--initial_artifacts', type=int, required=True, help="Number of initial artifacts deployed")
parser.add_argument('--final_artifacts', type=int, required=True, help="Number of final artifacts deployed")
parser.add_argument('--total_artifacts', type=int, required=True, help="Total number of artifacts to be deployed")
parser.add_argument('--start_time', type=str, required=True, help="Start time (format: 'Sep 5, 10:17:48 AM')")
parser.add_argument('--end_time', type=str, required=True, help="End time (format: 'Sep 9, 11:04:43 PM')")

# Parse the arguments
args = parser.parse_args()

# Calculate results
speed, days_remaining = calculate_deployment_speed(
    args.initial_artifacts, args.final_artifacts, args.total_artifacts, args.start_time, args.end_time)

# Print the results
print(f"The deployment speed is approximately {speed:.2f} artifacts per minute.")
print(f"Based on this speed, the deployment is estimated to be completed in approximately {days_remaining:.2f} days.")
