import csv
import json
import argparse
from datetime import datetime
import pytz

def convert_csv_to_json(csv_file, json_file):
    assets = []

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            # Construct the 'source' path
            source_path = f"{row['Repository']}/{row['Group']}/{row['Artifact']}/{row['Version']}/{row['file']}"

            # Convert the uploadDate to Unix timestamp in UTC
            upload_date = row['uploadDate']
            # Parse the uploadDate with timezone awareness
            upload_datetime = datetime.strptime(upload_date, "%a, %d %b %Y %H:%M:%S %Z")
            # Ensure the datetime is in UTC using pytz.UTC
            upload_datetime_utc = pytz.UTC.localize(upload_datetime)
            # Get the Unix timestamp
            upload_timestamp = int(upload_datetime_utc.timestamp())
           
            # Create the asset dictionary
            asset = {
                "source": source_path,
                "fileblobRef": "",
                "lastDownloaded": "null",
                "lastUpdated": str(upload_timestamp)
            }

            assets.append(asset)

    # Create the final JSON structure
    output = {
        "assets": assets
    }

    # Write the JSON file
    with open(json_file, 'w') as outfile:
        json.dump(output, outfile, indent=4)

def main():
    parser = argparse.ArgumentParser(description='Convert a CSV file to a JSON file.')
    parser.add_argument('csv_file', help='Path to the input CSV file')
    parser.add_argument('json_file', help='Path to the output JSON file')
    
    args = parser.parse_args()
    
    convert_csv_to_json(args.csv_file, args.json_file)

if __name__ == '__main__':
    main()
