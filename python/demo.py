import os
import json

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "assets", "data.json")
citation = dict([('title', "IBM"), ('description', "Free learning resources")])

with open(DATA_FILE, "a", encoding="utf-8") as f:
    new_json_string = json.dumps(citation, indent=1)
    
    if(os.path.getsize(DATA_FILE) == 0):
        f.write("[\n" + new_json_string)
    else:
        f.write("," + "\n" + new_json_string)

with open(DATA_FILE, "r+", encoding="utf-8") as f:
    lines = f.readlines()
    if lines[-1] == "}":
        f.write("\n]")        
       