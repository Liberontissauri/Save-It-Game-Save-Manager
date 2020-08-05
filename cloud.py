import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
import savefiles
from os import remove
from os.path import exists

class DataTransfer():
    def __init__(self):
        with open("./code.ini", "r") as file:
            self.secret = file.read()
        self.dbx = dropbox.Dropbox(self.secret)
    
    def sendsaves(self):
        to_send = savefiles.Savedata(".")
        to_send.compress()

        for entry in self.dbx.files_list_folder('').entries:
            if entry.name == "Savedata.zip":
                self.dbx.files_delete("/Savedata.zip")
                break

        with open("./Savedata.zip", "rb") as file:
            self.dbx.files_upload(file.read(), "/Savedata.zip")

        remove("./Savedata.zip")

    def getsaves(self):
        self.dbx.files_download_to_file("./Savedata.zip","/Savedata.zip")
        savedata = savefiles.Savedata("./Savedata.zip")
        savedata.decompress()

def setupoauth2file(code):
    auth_flow = DropboxOAuth2FlowNoRedirect("c02irh2snxzphs5", "p3fdzx55ae539q8")

    auth_flow.start()

    code = auth_flow.finish(code)

    with open("./code.ini","w") as file:
        file.write(code.access_token)
