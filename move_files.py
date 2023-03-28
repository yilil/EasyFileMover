import os
import shutil
import tkinter as tk
from functools import partial
from tkinter import filedialog, CENTER

path = {"src": None, "dest": None}


def get_dir(target):
    path[target] = filedialog.askdirectory(initialdir=os.path.expanduser('~/'))
    print(f"{target} is {path[target]}")


def move():
    file_extension, filename = get_input()
    if not file_extension or file_extension in place_holders:
        tk.messagebox.showwarning("Warning",
                                  "Please specify a file extension!")
        return

    if filename in place_holders:
        filename = None

    src = path["src"]
    dest = path["dest"]
    if src is None or dest is None:
        tk.messagebox.showwarning(
            "Warning", "Please specify source and destination directories!")
        return

    src_files = os.listdir(src)
    dest_files = os.listdir(dest)

    c = 0
    for file in src_files:
        if filename and not filename in file:
            continue

        if file.endswith(f'.{file_extension}'):
            if file in dest_files:
                option = tk.messagebox.askquestion(
                    'File Exist Error',
                    f"{file} already exists in destination directory, continue?",
                    icon='warning')
                if option == "no":
                    continue
            c += 1
            shutil.move(os.path.join(src, file), os.path.join(dest, file))

    tk.messagebox.showinfo(
        "Success",
        f"{c} files has been successfully moved from {src} to {dest}!")
    # print(f"{c} files has been successfully moved from {src} to {dest}!")


def get_input():
    return extension_input.get(), filename_input.get()


def clear_placeholder(event):
    target = event.widget

    if target.get() in place_holders:
        target.delete(0, tk.END)
        target.config(fg='white')


def restore_placeholder(event, place_holder):
    target = event.widget

    if target.get() == "":
        target.insert(0, place_holder)
        target.config(fg='gray')


root = tk.Tk()
window_height = 200
window_width = 500
root.config(height=window_height, width=window_width)

# frame = tk.Frame(root, bg="white")
# frame.place(relx=0.5, rely=0.5, anchor=CENTER)
# canvas = tk.Canvas(root, bg='white', height=100, width=100)
# canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

place_holders = [
    "file extension such as (jpg, pdf)", "keyword in filename (case sensitive)"
]

extension_input = tk.Entry(root)
extension_input.insert(0, place_holders[0])
extension_input.config(fg='gray', width=window_width)
extension_input.pack()
extension_input.bind("<FocusIn>", clear_placeholder)
extension_input.bind(
    "<FocusOut>", lambda event: restore_placeholder(event, place_holders[0]))

filename_input = tk.Entry(root)
filename_input.insert(0, place_holders[1])
filename_input.config(fg='gray', width=window_height)
filename_input.pack()
filename_input.bind("<FocusIn>", clear_placeholder)
filename_input.bind("<FocusOut>",
                    lambda event: restore_placeholder(event, place_holders[1]))

open_src_button = tk.Button(root,
                            text="Select Source Directory",
                            padx=10,
                            pady=5,
                            command=partial(get_dir, "src"))
open_dest_button = tk.Button(root,
                             text="Select Destination Directory",
                             padx=10,
                             pady=5,
                             command=partial(get_dir, "dest"))
confirm_button = tk.Button(root, text="Confirm", padx=10, pady=5, command=move)
open_src_button.pack(fill="x")
open_dest_button.pack(fill="x")
confirm_button.pack(fill="x")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# calculate position x, y
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

root.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))

root.mainloop()