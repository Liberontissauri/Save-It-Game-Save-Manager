from os import walk, getenv
from os.path import join

def get_paths_from_file():
    pathlist = []
    with open("./paths.ini", "r") as pathfile:
        for line in pathfile:
            if line[1] == ":":  # Detecting if a line is a path by checking if the second character is a colon (from C: ; D: ; etc)
                if line[-1:] == "\n":
                    pathlist.append(line[:-1])
                else:
                    pathlist.append(line)
    return pathlist

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
