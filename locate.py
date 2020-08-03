from os import walk, getenv
from os.path import join

def create_path_file():
    with open("./paths.ini", "w") as path_file:
        path_file.write("[Paths]\n")

def get_paths_in_save(path_to_save): # Returns a list of paths to all the files in a save folder
    file_list = []
    for root, _, files in walk(path_to_save, topdown=False):
        for file in files:
            file_list.append(join(root,file))
    return file_list

def replace_appdata_with_path(toreplace):
    return getenv("APPDATA") + toreplace[9:]
