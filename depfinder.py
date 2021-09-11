import os
import json
import shutil
import argparse
from zipfile import ZipFile
import glob

parser = argparse.ArgumentParser()
parser.add_argument("--var-path", type=str, required=True, help="The path to your main var directory.")
parser.add_argument("--move-broken", type=str, help="The path to move your broken vars to.")
parser.add_argument("--list", action="store_true", help="Output results as list of missing packagees instead of JSON.")
args = parser.parse_args()


var_list = list(glob.glob(os.path.join(args.var_path, "**", "*.var"), recursive=True))

var_list_string = "\n".join(var_list)  # Easier to search for substrings
missing_deps = {}
broken_deps = []
errors = []

for index, var in enumerate(var_list):
    print(f"Indexing... ({index}/{len(var_list)})", end="\r")
    try:
        with ZipFile(var, "r") as open_var:
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
                broken_deps.append(var)
                if var_name not in missing_deps:
                    missing_deps[var_name] = []
                missing_deps[var_name].append(key)

if args.move_broken:
    for broken_file in list(set(broken_deps)):
        target_path = os.path.join(args.move_broken, os.path.basename(broken_file))
        if os.path.exists(broken_file):
            shutil.move(broken_file, target_path)
        else:
            print(f"Somehow, {broken_file} wasn't found!")
    

if args.list:
    results = list(set(x for y in missing_deps.values() for x in y))
    result_string = "\n".join(results)
    result_file_name = "missing.txt"
else:
    results = dict(sorted(missing_deps.items(), key=lambda x: len(x[1]), reverse=True))       
    result_string = json.dumps(results, indent=4)
    result_file_name = "missing.json"
print(result_string)    
print("===")
print("Additionally, the following errors occured: " + "\n".join(errors))         
with open(result_file_name, "w", encoding="utf-8") as missing_file:
    missing_file.write(result_string)