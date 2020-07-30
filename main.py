from tkinter import *

class App:
    def __init__(self, master):
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

        self.save_list = Listbox(self.savefiles_frame, width = 70)
        self.save_list_scrollbar = Scrollbar(self.savefiles_frame)
        self.save_list.config(yscrollcommand = self.save_list_scrollbar.set)
        self.save_list_scrollbar.config(command = self.save_list.yview)

        self.button_add = Button(self.save_management, text = "Add", width = 10)
        self.button_delete = Button(self.save_management, text = "Delete", width = 10)
        self.entry_name = Entry(self.save_management, width = 40)
        self.entry_path = Entry(self.save_management, width = 40)
        self.button_find = Button(self.save_management, text = "Find", width = 10)

        self.button_send = Button(self.export_and_import_frame, text = "Send Saves", width = 10)
        self.button_load = Button(self.export_and_import_frame, text = "Load File", width = 10)

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
        self.button_find.grid(row = 0, column = 2, sticky = W)

        self.button_send.grid(row=0, pady = (0, 10))
        self.button_load.grid(row=1)

        # Layout configured

        self.menubar = Menu(master)

        self.filemenu = Menu(self.menubar)
        self.menubar.add_cascade(label = "File", menu=self.filemenu)

        self.configmenu = Menu(self.menubar)
        self.menubar.add_cascade(label = "Configuration", menu=self.configmenu)

        self.menubar.add_command(label="Exit", command=exit)
        
        
root = Tk()
application = App(root)
root.title("Save It! - Game Save Manager")
root.resizable(False,False)
root.config(menu=application.menubar)
root.mainloop()