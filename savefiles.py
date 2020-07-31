from os import mkdir, listdir
from os.path import isdir, exists
from shutil import copytree
import json
from zipfile import ZipFile
import locate

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

        if not exists(self.path):

            reversed_path = ""

            for char in self.path:
                reversed_path = char + reversed_path
            copytree(self.path, "./SaveData/"+self.path[-(reversed_path.find("/")):])

class Savedata():
    def __init__(self, path):
        self.path = path
        if ".zip" in self.path:
            self.iscompressed = True
        else:
            self.iscompressed = False
            
    def compress(self):
        if self.iscompressed == True:
            raise Exception("Savedata is already compressed")

        with ZipFile(self.path + "\\Savedata.zip","w") as zip:
            for file in locate.get_paths_in_save("./SaveData"):
                zip.write(file)
        
        self.iscompressed = True

    def decompress(self):
        if self.iscompressed == False:
            raise Exception("Savedata is already decompressed")

        with ZipFile(self.path, "r") as zip:
            zip.extractall()


def read_saveinfo():
    with open("./SaveData/saveinfo.json", "r") as saveinfo:
        loaded_saveinfo = json.load(saveinfo)
        return loaded_saveinfo

def write_saveinfo(data):
    with open("./SaveData/saveinfo.json", "w") as saveinfo:
        json.dump(data,saveinfo)
