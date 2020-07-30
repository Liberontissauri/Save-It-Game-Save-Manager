from os import mkdir, listdir
from os.path import isdir, exists
import json

class Savefile():
    def __init__(self, name, path):
        self.path = path
        self.name = name

        if not isdir("./SaveData"):
            mkdir("./SaveData")
        
        if not exists("./SaveData/saveinfo.json"):
            with open("./SaveData/saveinfo.json", "w") as saveinfo:
                saveinfo.write(json.dumps({}))

        loaded_saveinfo = read_saveinfo()
        loaded_saveinfo[self.name] = self.path

        write_saveinfo(loaded_saveinfo)

def read_saveinfo():
    with open("./SaveData/saveinfo.json", "r") as saveinfo:
        loaded_saveinfo = json.load(saveinfo)
        return loaded_saveinfo

def write_saveinfo(data):
    with open("./SaveData/saveinfo.json", "w") as saveinfo:
        json.dump(data,saveinfo)


    