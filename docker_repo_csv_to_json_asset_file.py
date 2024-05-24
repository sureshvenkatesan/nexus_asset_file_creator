import json
import sys

def main():
    input_file = "/Users/angellom/Downloads/atnt/az-asset-list.csv"
    output_file = "/Users/angellom/Downloads/atnt/docker3.json"
    out_json = {"assets":{"blob":[], "manifestV1":[], "manifestV2":[]}}

    with open(input_file, 'r') as list_file:
        for line in list_file:
            list_line = line.split(",")

            try:
                path = list_line[6]
            except:
                print ("ERROR")
                print(line)
                continue
            if "v1/repositories" in path:
                print(path)
                continue
            else:
                if "manifests" in path:
                    adigest = "sha256:"+list_line[2]
                    if "sha256:" in path:
                        digest = path.split("/")[-1]
                        data = {
                            "source": "docker-hosted/" + path.rstrip(),
                            "fileblobRef": "",
                            "digest": digest
                        }
                        out_json["assets"]["manifestV2"].append(data)
                    else:
                        data = {
                            "source": "docker-hosted/" + path.rstrip(),
                            "fileblobRef": "",
                            "digest": adigest
                        }
                        out_json["assets"]["manifestV1"].append(data)
                else:
                    data = {
                        "source": "docker-hosted/"+path.rstrip(),
                        "fileblobRef": ""
                    }
                    out_json["assets"]["blob"].append(data)

        with open(output_file, 'w') as fp:
            json.dump(out_json, fp)


if __name__ == '__main__':
    main()