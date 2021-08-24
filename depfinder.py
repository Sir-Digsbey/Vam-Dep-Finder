import os
import json
import argparse
from zipfile import ZipFile
import glob

parser = argparse.ArgumentParser()
parser.add_argument("--var-path", type=str, required=True, help="The path to your main var directory.")
parser.add_argument("--list", action="store_true", help="Output results as list of missing packagees instead of JSON.")
args = parser.parse_args()


var_list = list(glob.glob(os.path.join(args.var_path, "**", "*.var"), recursive=True))

required_dependencies = []
var_list_string = "\n".join(var_list)
missing_deps = {}
errors = []

for index, var in enumerate(var_list):
    print(f"Indexing... ({index}/{len(var_list)})", end="\r")
    try:
        open_var = ZipFile(var, "r")
        json_string = open_var.read('meta.json')
        json_data = json.loads(json_string)
    except Exception as ex:
        errors.append(var + f" ({str(ex)})")
        continue
    if deps := json_data.get("dependencies"):
        for key in deps:
            key = key.replace(".latest", "")
            if key not in var_list_string:
                var_name = os.path.basename(var)
                if var_name not in missing_deps:
                    missing_deps[var_name] = []
                missing_deps[var_name].append(key)             

if args.list:
    results = list(set(x for y in missing_deps.values() for x in y))
    result_string = "\n".join(results)
    result_file_name = "missing.txt"
else:
    results = {k:v for k, v in sorted(missing_deps.items(), key=lambda x: len(x[1]), reverse=True)}       
    result_string = json.dumps(results, indent=4)
    result_file_name = "missing.json"
print(results)    
print("===")
print("Additionally, the following errors occured: " + "\n".join(errors))         
with open(result_file_name, "w", encoding="utf-8") as missing_file:
    missing_file.write(result_string)