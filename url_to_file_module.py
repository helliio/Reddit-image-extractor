import json
import os

def write_dict(name, path, data):
    mk_save_dir(path)
    with open(path + "/" + name + ".json", "w") as f:
        json.dump(data, f)

def mk_save_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir + "/"
