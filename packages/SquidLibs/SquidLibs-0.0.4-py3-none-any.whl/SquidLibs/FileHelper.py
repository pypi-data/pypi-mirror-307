import os, sys
from tkinter import filedialog

class FileHelper:
    def __init__(self):
        """Store file paths in paths to access anywhere else"""
        self.paths = {
            'base_path' : os.path.dirname(os.path.dirname(sys.argv[0])),
            'internals_path' : os.path.dirname(os.path.abspath(__file__)),
            'lang_path' : ''
        }
        print(self.paths)
    def saveToFiletype(self, dataList, type, typeName):
        """Save each item from dataList to a new line in a file with a custom type."""
        file_path = filedialog.asksaveasfilename(defaultextension=f".{type}", filetypes=[(typeName, f"*.{type}")])
        if file_path:
            with open(file_path, 'w') as file:
                for item in dataList:
                    file.write(f"{item}\n")

    def loadFromFiletype(self, type, typeName):
        """Open a file and read its contents into a list, each line being an item."""
        file_path = filedialog.askopenfilename(filetypes=[(typeName, f"*.{type}")])
        if file_path:
            with open(file_path, 'r') as file:
                dataList = [line.strip() for line in file]
            return dataList

    def safe_open_w(self, path, mode='w', newline='',encoding=None):
        """Open `path` for writing (by default), creating any parent directories as needed."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return open(path, mode, newline=newline,encoding=encoding)