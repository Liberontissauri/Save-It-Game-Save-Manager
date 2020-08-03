from os import mkdir, listdir, remove
from os.path import isdir, exists
from shutil import copytree, rmtree
import json
from zipfile import ZipFile
import locate

def verify_initial_files():
    if not isdir("./SaveData"):
            mkdir("./SaveData")
        
    if not exists("./SaveData/saveinfo.json"):
        with open("./SaveData/saveinfo.json", "w") as saveinfo:
            saveinfo.write(json.dumps({}))

def copy_save_to_program_folder(save_path):
    if "%appdata%" in save_path:
        save_path = locate.replace_appdata_with_path(save_path)

    if exists(save_path):

        if not exists("./SaveData/" + get_folder_name(save_path)):
            copytree(save_path, "./SaveData/" + get_folder_name(save_path))
        else:
            rmtree("./SaveData/" + get_folder_name(save_path))
            copytree(save_path, "./SaveData/" + get_folder_name(save_path))

def copy_stored_save_to_game_save_location(savename):
    saveinfo = read_saveinfo()
    save_path = saveinfo[savename]

    if "%appdata%" in save_path:
        save_path = locate.replace_appdata_with_path(save_path)

    stored_savepath = "./SaveData/" + get_folder_name(save_path)

    if exists(save_path):
        rmtree(save_path)
    copytree(stored_savepath, save_path)

def reverse_string(string):
    reversed_str = ""
    for char in string:
        reversed_str = char + reversed_str
    return reversed_str

def get_folder_name(path):
    return path[-(reverse_string(path).find("\\")):]

def update_program_save_folder():
    saveinfo = read_saveinfo()
    for folder in listdir(".\\SaveData\\"):
        if "." not in folder:
            rmtree(".\\SaveData\\" + folder)
    for name in saveinfo:
        copy_save_to_program_folder(saveinfo[name])

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

        rmtree("./SaveData")

        with ZipFile(self.path, "r") as zip:
            zip.extractall()


def read_saveinfo():
    with open("./SaveData/saveinfo.json", "r") as saveinfo:
        loaded_saveinfo = json.load(saveinfo)
        return loaded_saveinfo

def write_saveinfo(data):
    with open("./SaveData/saveinfo.json", "w") as saveinfo:
        json.dump(data,saveinfo)
