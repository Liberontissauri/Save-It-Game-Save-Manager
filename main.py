from tkinter import Tk, Frame, SUNKEN, RAISED, Listbox, SINGLE, Scrollbar, Button, \
    Entry, W, LEFT, RIGHT, Menu, END, Label, ACTIVE, ANCHOR, Toplevel
    
from tkinter import filedialog
import savefiles
from webbrowser import open_new
import cloud
from locate import replace_appdata_with_path

class App:
    def __init__(self, master):
        savefiles.verify_initial_files()

        # Beginning of the creation of the frames

        self.main_frame = Frame(master)
        self.savefiles_frame = Frame(self.main_frame)
        self.export_and_import_frame = Frame(self.main_frame)
        self.save_management = Frame(self.main_frame)

        # The frames are created


        # Beginning of the frames's configuration

        self.savefiles_frame.config(borderwidth = 4, relief = SUNKEN, padx = 15, pady = 20)
        self.export_and_import_frame.config(borderwidth = 3, relief = RAISED, padx = 20, pady = 120)
        self.save_management.config(borderwidth = 3, relief = RAISED, padx = 10, pady = 10)

        # Configuration finished


        # Beginning of the creation of the widgets

        self.save_list = Listbox(self.savefiles_frame, selectmode = SINGLE, width = 70)
        self.save_list_scrollbar = Scrollbar(self.savefiles_frame)
        self.save_list.config(yscrollcommand = self.save_list_scrollbar.set)
        self.save_list_scrollbar.config(command = self.save_list.yview)
        self.save_list.bind('<<ListboxSelect>>',self.update_entrys)

        self.button_add = Button(self.save_management, text = "Add", command = self.open_add_save_window, width = 10)
        self.button_delete = Button(self.save_management, text = "Delete", command = self.delete_element, width = 10)
        self.entry_name = Entry(self.save_management, width = 40)
        self.entry_path = Entry(self.save_management, width = 40)
        self.button_update = Button(self.save_management, text = "Update", command = self.update_config, width = 10)
        self.button_find = Button(self.save_management, text = "Find", command = self.find_openfolder_path, width = 10)

        self.button_send = Button(self.export_and_import_frame, text = "Send Saves", command = self.send_files, width = 10)
        self.button_load = Button(self.export_and_import_frame, text = "Import Data", command = self.import_compressed_savedata, width = 10)
        self.button_export = Button(self.export_and_import_frame, text = "Export Data", command = self.export_savedata, width = 10)
        self.button_send_to_cloud = Button(self.export_and_import_frame, text = "Send to cloud", command = self.send_files_to_cloud, width = 13)
        self.button_get_from_cloud = Button(self.export_and_import_frame, text = "get from cloud", command = self.get_files_from_cloud, width = 13)
        # The widgets are created


        # Beginning of the configuration of the layout

        self.main_frame.grid(sticky = W)
        self.savefiles_frame.grid(row = 0, column = 0, padx = 30, pady = (20, 0))
        self.export_and_import_frame.grid(row = 0, column = 1, rowspan = 2, padx = (0,30))
        self.save_management.grid(row=1, column = 0, sticky = W, padx = 30, pady = (10,20))

        self.save_list.pack(side=LEFT)
        self.save_list_scrollbar.pack(side = RIGHT, fill="y")

        self.button_add.grid(row = 0, column = 0, pady = 5, sticky = W)
        self.button_delete.grid(row = 1, column = 0, sticky = W)
        self.entry_name.grid(row = 0, column = 1, padx = (10,10), sticky = W)
        self.entry_path.grid(row = 1, column = 1, padx = (10,10), sticky = W)
        self.button_update.grid(row = 0, column = 2, sticky = W)
        self.button_find.grid(row = 1, column = 2, sticky = W)

        self.button_send.grid(row = 0, pady = (0, 10))
        self.button_load.grid(row = 1, pady = (0, 10))
        self.button_export.grid(row = 2, pady = (0, 10))
        self.button_get_from_cloud.grid(row = 3, pady = (0, 10))
        self.button_send_to_cloud.grid(row = 4)

        # Layout configured


        # Beginning of the creation of the MenuBar

        self.menubar = Menu(master)

        self.filemenu = Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label = "File", menu=self.filemenu)
        self.filemenu.add_command(label="Import Data", command=self.import_compressed_savedata)
        self.filemenu.add_command(label="Export Data", command=self.export_savedata)
        self.filemenu.add_command(label="Exit", command=master.destroy)

        self.configmenu = Menu(self.menubar, tearoff = 0)
        self.configmenu.add_command(label="Configure dropbox", command=self.open_dropbox_window)
        self.menubar.add_cascade(label = "Configuration", menu=self.configmenu)

        self.menubar.add_command(label="Exit", command=master.destroy)

        # MenuBar Created

        self.add_save_window_is_open = False
        self.dropbox_window_is_open = False
        self.last_active = None

        self.update_save_list()
        
    def update_save_list(self):
        self.save_list.delete(0,END)
        for name in savefiles.read_saveinfo():
            self.save_list.insert(END, name)
        savefiles.update_program_save_folder()

    def delete_element(self):
        saveinfo = savefiles.read_saveinfo()
        saveinfo.pop(self.save_list.get(ACTIVE))
        savefiles.write_saveinfo(saveinfo)
        self.update_save_list()

    def update_entrys(self, evt):
        if self.save_list.get(ANCHOR) != "":
            self.entry_name.delete(0,END)
            self.entry_name.insert(0,self.save_list.get(ANCHOR))
            self.entry_path.delete(0,END)
            self.entry_path.insert(0,savefiles.read_saveinfo()[self.save_list.get(ANCHOR)])
            self.last_active = self.save_list.get(ANCHOR)

    def find_openfolder_path(self):
        openfolder_path = filedialog.askdirectory(initialdir = "/", title = "Select Save Folder")
        if openfolder_path != "":
            self.entry_path.delete(0,END)
            self.entry_path.insert(0,openfolder_path)
        
    def import_compressed_savedata(self):
        savedatafolder_path = filedialog.askopenfilename(initialdir = "./", title = "Select Compressed SaveData File", filetypes = (("zip files","*.zip"),("all files","*.*")))
        if savedatafolder_path != "":
            savedata_file = savefiles.Savedata(savedatafolder_path)
            savedata_file.decompress()
        self.update_entrys("event")
        self.update_save_list()

    def export_savedata(self):
        toexport_location = filedialog.askdirectory(initialdir = "./", title = "Select Export Location")
        savedata_file = savefiles.Savedata(toexport_location)
        savedata_file.compress()

    def update_config(self):
        saveinfo = savefiles.read_saveinfo()
        if self.last_active != None:
            saveinfo.pop(self.last_active)
        if self.entry_name.get() != "":
            saveinfo[self.entry_name.get()] = self.entry_path.get()
            savefiles.write_saveinfo(saveinfo)
            self.last_active = self.entry_name.get()
        self.update_save_list()

    def open_add_save_window(self):
        def add_save():
            if entry_name.get() != "" and entry_path.get() != "":
                saveinfo = savefiles.read_saveinfo()
                if "%appdata%" in entry_path.get():
                    saveinfo[entry_name.get()] = replace_appdata_with_path(entry_path.get())
                else:
                    saveinfo[entry_name.get()] = entry_path.get()
                    
                savefiles.write_saveinfo(saveinfo)
                self.update_save_list()
                self.close_add_save_window()

        def find_add_window_openfolder_path():
            openfolder_path = filedialog.askdirectory(initialdir = "/", title = "Select Save Folder")
            if openfolder_path != "":
                entry_path.delete(0,END)
                entry_path.insert(0,openfolder_path)

        if self.add_save_window_is_open == False:
            self.add_save_window = Toplevel(self.main_frame)
            self.add_save_window_is_open = True
            self.add_save_window.protocol("WM_DELETE_WINDOW",self.close_add_save_window)

            label_name = Label(self.add_save_window, text = "Name")
            label_path = Label(self.add_save_window, text = "Path")

            entry_name = Entry(self.add_save_window, width = 50)
            entry_path = Entry(self.add_save_window, width = 50)

            button_add = Button(self.add_save_window, command = add_save, text = "Add", width = 6)
            button_cancel = Button(self.add_save_window, command = self.close_add_save_window, text = "Cancel", width = 6)
            button_find = Button(self.add_save_window, command = find_add_window_openfolder_path, text = "Find", width = 6)

            label_name.grid(row = 0, column = 0, padx = (10,5), pady = (17,3))
            label_path.grid(row = 1, column = 0, pady = (0,3))
            entry_name.grid(row = 0, column = 1, padx = (0,20), pady = (17,3))
            entry_path.grid(row = 1, column = 1, padx = (0,20), pady = (0,3))
            button_add.grid(row = 2, column = 0, padx = (10,0), pady = (7,0))
            button_cancel.grid(row = 4, column = 0, padx = (10,0), pady = (5,5))
            button_find.grid(row = 3, column = 0, padx = (10,0), pady = (7,0))

    def close_add_save_window(self):
        self.add_save_window_is_open = False
        self.add_save_window.destroy()

    def open_dropbox_window(self):
        def update_dropbox_config():
            cloud.setupoauth2file(entry_code.get())

        if self.dropbox_window_is_open == False:
            self.dropbox_window = Toplevel(self.main_frame)
            self.dropbox_window_is_open = True
            self.dropbox_window.protocol("WM_DELETE_WINDOW",self.close_dropbox_window)

            label_code = Label(self.dropbox_window, text = "Enter the code:")
            entry_code = Entry(self.dropbox_window, width = 70)
            button_update_cloud = Button(self.dropbox_window, command = update_dropbox_config, text = "Update")
            label_instructions = Label(self.dropbox_window, text = "Copy the code given by the link below")
            label_oauthlink = Label(self.dropbox_window, text = "https://www.dropbox.com/oauth2/authorize?response_type=code&client_id=c02irh2snxzphs5")
            label_oauthlink.bind("<Button-1>", lambda e: open_new("https://www.dropbox.com/oauth2/authorize?response_type=code&client_id=c02irh2snxzphs5"))

            label_code.grid(row = 0, column = 0, sticky = W, padx = (10,5), pady = (10,0))
            entry_code.grid(row = 0, column = 1, pady = (10,0))
            button_update_cloud.grid(row = 1, column = 0, sticky = W, padx = (10,5))
            label_instructions.grid(row = 1, column = 1)
            label_oauthlink.grid(row = 2, column = 0, columnspan = 2, padx = 10, pady = (5,10))

    def close_dropbox_window(self):
        self.dropbox_window_is_open = False
        self.dropbox_window.destroy()

    def send_files(self):
        saveinfo = savefiles.read_saveinfo()

        for name in saveinfo:
            savefiles.copy_stored_save_to_game_save_location(name)

    def send_files_to_cloud(self):
        with open("./code.ini", "r") as file:
            code = file.read()
        cloud_transfer = cloud.DataTransfer(code)
        cloud_transfer.sendsaves()

    def get_files_from_cloud(self):
        with open("./code.ini", "r") as file:
            code = file.read()
        cloud_transfer = cloud.DataTransfer(code)
        cloud_transfer.getsaves()



root = Tk()
application = App(root)
root.title("Save It! - Game Save Manager")
root.resizable(False,False)
root.config(menu=application.menubar)
root.mainloop()