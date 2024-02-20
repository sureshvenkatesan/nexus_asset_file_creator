import argparse
import json

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process input and output files.")
    parser.add_argument("--input-file", help="Input CSV file path", default="/Users/angellom/Downloads/maven_artifacts.csv")
    parser.add_argument("--output-file", help="Output JSON file path", default="/Users/angellom/Downloads/assetmap.json")
    parser.add_argument("--output-path", help="Output directory path", default="/Users/angellom/Downloads/atnt/test_json")
    return parser.parse_args()

def process_input(input_file):
    out_json_per_repo = {}
    alist = []
    with open(input_file, 'r') as list_file:
        for path in list_file:
            path_list = path.split(",")
            repo_name = path_list[0]
            path = path_list[0] + path_list[1]
            path = path.rstrip()
            data = {
                "source": path,
                "fileblobRef": ""
            }
            if repo_name in alist:
                out_json_per_repo[repo_name]["assets"].append(data)
            else:
                out_json_per_repo[repo_name] = {"assets": [data]}
                alist.append(repo_name)
    return out_json_per_repo

def write_output(out_json_per_repo, output_path):
    for repo, data in out_json_per_repo.items():
        output_file = output_path + "/" + repo + "_assetmap.json"
        with open(output_file, 'w') as fp:
            json.dump(data, fp)

def main():
    args = parse_arguments()
    out_json_per_repo = process_input(args.input_file)
    write_output(out_json_per_repo, args.output_path)
    print(f"Output files have been written to {args.output_path}")

if __name__ == '__main__':
    main()
