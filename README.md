# Save It - Game Save Manager
A program to manage game save data.

### Features

- Import and export savedata;
- Automatically copy the savedata stored in the program folder to the respective paths (Not Implemented);
- Send the savedata to google drive (Not Implemented).

![demo1]( ./img/demo1.gif)

### Dependencies

- Python 3;
- The modules imported are part of the standard library;
- pyinstaller (only if you build the program yourself).

### Building

- clone the repository;

> git clone https://github.com/Liberontissauri/Save-It-Game-Save-Manager.git

- On the cloned folder, run:

> pyinstaller -onefile main.py

- The program should be on:

> ./dist

### License

This software is licensed under the MIT License.