from tkinter import *
import tkinter as tk
from tkinter import filedialog as fd
import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from tkinter.filedialog import asksaveasfile

file1 = None
toFile = None

# create the root window
root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry('400x150')


def save3():
    global file1
    # Convert the pandas DataFrame to a pyarrow Table
    table = pa.Table.from_pandas(file1)

    # Save the pyarrow Table as ORC
    
    filesave2 = asksaveasfile(mode='wb', defaultextension=".orc")
    if filesave2:
        pq.write_table(table, filesave2)

def save2():
    global file1
    global toFile
    filesave1 = asksaveasfile(mode='w', defaultextension=".txt")
    if filesave1:
        completeName = filesave1.name
        file1 = open(completeName, "w")
        file1.write(toFile)
        file1.close()

def save():
    global file1
    filesave = asksaveasfile(mode='w', defaultextension=".json")
    if filesave:
        file1.to_json(filesave.name)

def show():
    global file1
    global toFile
    word = clicked_save.get()
    if word == "json":
        save()
    if word == "text":
        save2()
    if word == "orc":
        save3()

def select_file():
    global file1
    global toFile
    filetypes = (
        ('CSV files', '*.csv'),
        ('Text files', '*.txt'),
        ('JSON files', '*.json'),
        ('All files', '*.*')
    )
    filename = fd.askopenfilename(filetypes=filetypes)
    if filename:

        ext = clicked_open.get()
        #ext = os.path.splitext(filename)[-1].lower()
        if ext == 'CSV files (*.csv)':
            file1 = pd.read_csv(filename)
        elif ext == 'Text files (*.txt)':
            file1 = pd.read_csv(filename, sep='\t')
        elif ext == 'JSON files (*.json)':
            file1 = pd.read_json(filename)

        toFile = file1.to_string(index=False)
        # Print the content to verify it has been read successfully
        # print(file1)

# Frame for opening files
frame_open = Frame(root)
frame_open.pack()

def select_folder():
    foldername = fd.askdirectory()
    print("Selected Folder:", foldername)

# Dropdown menu options for saving
options_save = [
    "json",
    "text",
    "orc",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]


# Frame for saving files
frame_save = Frame(root)
frame_save.pack()

# datatype of menu text for saving
clicked_save = StringVar()
clicked_save.set("json")

# Create Dropdown menu for saving
drop_save = OptionMenu(root, clicked_save, *options_save)
drop_save.pack(side = "right")

# Create button to save
button_save = Button(root, text="Save", command=show)
button_save.pack(side = "right")

# Create Label for saving
#label_save = Label(root, text=" ")
#label_save.pack()

# Dropdown menu options for opening files of different formats
options_open = [
    "CSV files (*.csv)",
    "Text files (*.txt)",
    "JSON files (*.json)",
    "All files (*.*)"
]

# datatype of menu text for opening files
clicked_open = StringVar()
clicked_open.set(options_open[0])  # Set the default option

# Create Dropdown menu for opening files
drop_open = OptionMenu(root, clicked_open, *options_open)
drop_open.pack(side ="left")

# Create open file button
open_button = Button(root, text="Open a File", command=select_file)
open_button.pack(side = "left")

# Create open folder button
#folder_button = Button(root, text="Open a Folder", command=select_folder)
#folder_button.pack()

# Execute tkinter
root.mainloop()
