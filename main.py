from frontEnd import ClientApp
import tkinter as tk
from tkinter import messagebox
"""
Asking the user for his/her name 
and creating a new ClientApp instance
"""
start_win = tk.Tk()
start_win.geometry('480x300')
start_win.title('Login')
start_win.configure()
promt = tk.Label(start_win, text='Name:', font=("Times New Roman", 15))
promt.place(x=10, y=50, height=50, width=200)
name_entry = tk.Entry(start_win, font=("Times New Roman", 15))
name_entry.place(x=250, y=50, height=50, width=200)


def enter_chat():
    name = name_entry.get()
    if name:
        if name.isalpha():
            start_win.destroy()
            ClientApp(name)
        else:
            messagebox.showwarning("Improper Name", "Invalid name")
    else:
        messagebox.showwarning("Improper Name", "Null name")


start_btn = tk.Button(start_win, text='Enter Chat!', font=("Times New Roman", 15),
                      command=enter_chat)
start_btn.place(x=195, y=180, height=50, width=100)
start_win.mainloop()
