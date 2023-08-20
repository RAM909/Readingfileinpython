from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import os
import yaml
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from tkinter.filedialog import asksaveasfile
from pymongo import MongoClient
import json

file1 = None
toFile = None

# create the root window
root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry("600x400")
root.configure(bg="#4187c7")


def savingdb():
    global file1
    client = MongoClient('mongodb://localhost:27017/')
    db = client['yash']
    collection = db['json']


    json_data = file1.to_json(orient='records')

    data = json.loads(json_data)
    collection.insert_many(data)
    show_success_prompt1()

def show_success_prompt():
    success_prompt = tk.Toplevel(root)
    success_prompt.title('Success')
    success_prompt.geometry('200x50')
    label = tk.Label(success_prompt, text='Saved successfully')
    label.pack()
    # Destroy the success_prompt after a short delay (e.g., 2 seconds)
    success_prompt.after(2000, success_prompt.destroy)


def show_success_prompt1():
  success_prompt1 = tk.Toplevel(root)
  success_prompt1.title('Success')
  success_prompt1.geometry('300x100')
  label = tk.Label(success_prompt1, text='Uploaded successfully')
  label.pack()
  # Destroy the success_prompt after a short delay (e.g., 2 seconds)
  success_prompt1.after(2000, success_prompt1.destroy)


def save5():
    global file1

    # Convert the DataFrame to a Python dictionary
    data_dict = file1.to_dict(orient='records')
    filesave4 = asksaveasfile(mode='w', defaultextension=".yaml")
    if filesave4:
     filepath = filesave4.name 
    # Write the data to a YAML file
     with open(filepath, "w") as f:
      yaml.dump(data_dict, f)
    show_success_prompt()

def save4():
    global file1
    # Convert the pandas DataFrame to a pyarrow Table
    table = pa.Table.from_pandas(file1)

    # Save the pyarrow Table as ORC
    
    filesave3 = asksaveasfile(mode='wb', defaultextension=".parquet")
    if filesave3:
        pq.write_table(table, filesave3)
    show_success_prompt()



def save3():
    global file1
    # Convert the pandas DataFrame to a pyarrow Table
    table = pa.Table.from_pandas(file1)

    # Save the pyarrow Table as ORC
    
    filesave2 = asksaveasfile(mode='wb', defaultextension=".orc")
    if filesave2:
        pq.write_table(table, filesave2)
    show_success_prompt()


def save2():
    global file1
    global toFile
    filesave1 = asksaveasfile(mode='w', defaultextension=".txt")
    if filesave1:
        completeName = filesave1.name
        file1 = open(completeName, "w")
        file1.write(toFile)
        file1.close()
    show_success_prompt()


def save():
    global file1
    filesave = asksaveasfile(mode='w', defaultextension=".json")
    if filesave:
        file1.to_json(filesave.name)
    show_success_prompt()
   

def show():
    global file1
    global toFile
    word = store.get()
    if word == "JSON":
        save()
    if word == "TEXT":
        save2()
    if word == "ORC":
        save3()
    if word == "PARQUET":
        save4()
    if word == "YAML":
        save5()

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

        ext = open_combobox.get()
        #ext = os.path.splitext(filename)[-1].lower()
        if ext == 'CSV FILE':
            file1 = pd.read_csv(filename)
        elif ext == 'TEXT FILE':
            file1 = pd.read_csv(filename, sep='\t')
        elif ext == 'JSON FILE':
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

#/ Dropdown menu options for saving
"""options_save = [
    "json",
    "text",
    "orc",
    "parquet",
    "yaml",
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
drop_save.pack(side = "right")"""

Top_Frame=Frame(root,bg="#FFFFB9",width=600,height=70)
Label(Top_Frame,text="~FILE CONVERTER~",font="Constantia 30 italic",bg="#FFFFB9",fg="black").place(x=100,y=10)
Top_Frame.place(x=0,y=0)


store = ttk.Combobox(root, values=["JSON","TEXT","ORC","PARQUET","YAML"], font="Constantia 15 ", state='readonly', width=15)
store.place(x=400, y=100)
store.set('SELECT FILE')


# Create button to save
button_save = Button(root, text="Save", width =10 ,font = "Constantia 17 bold", command=show)
button_save.place(x=420,y=180)

# Create Label for saving
#label_save = Label(root, text=" ")
#label_save.pack()

# Dropdown menu options for opening files of different formats
"""options_open = [
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
drop_open.pack(side ="left")"""

open_combobox = ttk.Combobox(root, values=["CSV FILE","JSON FILE","TEXT FILE"], font="Constantia 15 ", state='readonly', width=15)
open_combobox.place(x=30, y=100)
open_combobox.set('SELECT FILE')

# Create open file button
open_button = Button(root, text="Open File", width = 10 ,font = "Constantia 17 bold", command=select_file)
open_button.place(x=45,y=180)


upload = Button(root, text="UPLOAD", width =10 ,font = "Constantia 17 bold",command = savingdb)
upload.place(x=220,y=300)

Label(root, text=">>>>>>>", font="Constantia 25 bold", bg= "#4187c7", fg="black").place(x=248, y=95)
Label(root, text="CONVERT TO", font="Constantia 15 bold", bg= "#4187c7", fg="black").place(x=248, y=85)



# Create open folder button
#folder_button = Button(root, text="Open a Folder", command=select_folder)
#folder_button.pack()

# Execute tkinter
root.mainloop()
