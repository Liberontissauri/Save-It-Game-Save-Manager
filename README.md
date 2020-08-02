# Save It - Game Save Manager
A program to manage game save data.

### Features

- Import and export savedata;
- Automatically copy the savedata stored in the program folder to the respective paths;
- Create backups of the stored data in zip files;
- Import those same files into the program from another computer;
- Send the savedata to dropbox (Not Implemented).

![demo1](https://i.imgur.com/JMP5RpF.png)

### Dependencies

- Python 3;
- The modules imported are part of the standard library;
- pyinstaller (only if you build the program yourself).

### Building

- clone the repository;

> git clone https://github.com/Liberontissauri/Save-It-Game-Save-Manager.git

- On the cloned folder, run:

> pyinstaller --onefile --noconsole main.py

- The program should be on:

> ./dist

### License

This software is licensed under the MIT License.
