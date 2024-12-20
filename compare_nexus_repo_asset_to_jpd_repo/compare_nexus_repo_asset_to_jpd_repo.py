import json
import argparse

def load_json_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def write_to_json_file(filename, sources, assetmap_data):
    # Create a mapping of source to full asset data
    source_to_asset = {asset['source']: asset for asset in assetmap_data['assets']}
    
    # Create output structure
    output = {
        "assets": [
            source_to_asset[source] for source in sources
        ]
    }
    
    # Write JSON file
    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Compare repository assets and generate mismatch reports')
    parser.add_argument('--east-json', required=True, help='Path to the east JSON file')
    parser.add_argument('--assetmap-json', required=True, help='Path to the assetmap JSON file')
    parser.add_argument('--repo-name', required=True, help='Repository name (e.g., corp_releases)')
    
    args = parser.parse_args()

    # Load both JSON files
    east_data = load_json_file(args.east_json)
    assetmap_data = load_json_file(args.assetmap_json)

    # Create sets for efficient lookup
    east_sha1s = {file['sha1'] for file in east_data['files']}
    east_uri_to_sha1 = {file['uri']: file['sha1'] for file in east_data['files']}

    # Lists to store mismatches
    sha1_mismatches = []
    source_mismatches = []

    repo_prefix = args.repo_name + '/'

    # Process each asset in assetmap
    for asset in assetmap_data['assets']:
        # Check if nexusAssetSha1 exists in east_sha1s
        if asset['nexusAssetSha1'] not in east_sha1s:
            sha1_mismatches.append(asset['source'])

        # Strip repo prefix and check path/sha1 match
        source_path = asset['source']
        if source_path.startswith(repo_prefix):
            stripped_path = '/' + source_path[len(repo_prefix):]
            
            # Check if path exists in east_uri_to_sha1 and compare SHA1s
            if stripped_path in east_uri_to_sha1:
                if east_uri_to_sha1[stripped_path] != asset['nexusAssetSha1']:
                    source_mismatches.append(source_path)
            else:
                # Path exists in Nexus but not in East
                source_mismatches.append(source_path)

    # Construct output filenames using repo name
    sha1_output = f'nexusAssetSha1_not_in_{args.repo_name}_east.json'
    source_output = f'nexus_source_not_in_{args.repo_name}_east.json'
    delta_output = f'{args.repo_name}_assetmap_delta.json'

    # Write individual mismatch files
    write_to_json_file(sha1_output, sha1_mismatches, assetmap_data)
    write_to_json_file(source_output, source_mismatches, assetmap_data)

    # Combine unique sources from both mismatch lists for the delta file
    all_mismatches = list(set(sha1_mismatches + source_mismatches))
    write_to_json_file(delta_output, all_mismatches, assetmap_data)

if __name__ == "__main__":
    main()