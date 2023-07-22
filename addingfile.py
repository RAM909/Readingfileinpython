import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import os
import pandas as pd
from tkinter.filedialog import asksaveasfile

file1 = None

# create the root window
root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry('300x150')

def save():
    global file1  # Access the global variable
    filesave = asksaveasfile()
    if filesave:
        file1.to_json(filesave)

def select_file():
    global file1  # Access the global variable

    filename = fd.askopenfilename()
    file1 = pd.read_csv(filename)

    # Print the content to verify it has been read successfully
    #print(file1)

    root = tk.Tk()
    root.geometry('200x150')

    btn = ttk.Button(
        root,
        text='Save',
        command=save
    )
    btn.pack(expand=True)
    root.mainloop()


# open button
open_button = ttk.Button(
    root,
    text='Open a File',
    command=select_file
)

open_button.pack(expand=True)

# run the application
root.mainloop()
