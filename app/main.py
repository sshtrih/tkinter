import tkinter as tk
import tkinter.messagebox as mb

from pymongo.errors import OperationFailure, InvalidURI
from tkinter import ttk

from app import store_db

from app.main_window import MainWindow

authorization_window = tk.Tk()
authorization_window.title('Sign in')
authorization_window.geometry("300x300")


def click():
    try:
        # user = store_db.User(l_username.get(), l_password.get(), l_database.get())
        user = store_db.User('ppetrov', '123', 'hardware_store')
        window = MainWindow(user)
        # authorization_window.destroy()
    except OperationFailure as e:
        mb.showerror('Error', str(e))
    except InvalidURI as e:
        mb.showerror('Error', str(e))


l_input_username = ttk.Label(authorization_window, text='Username')
l_username = ttk.Entry(authorization_window)
l_input_password = ttk.Label(authorization_window, text='Password')
l_password = ttk.Entry(authorization_window, show='*')
l_input_database = ttk.Label(authorization_window, text='Database')
l_database = ttk.Combobox(authorization_window, values=['admin', 'hardware_store'])
l_sign_in = ttk.Button(authorization_window, text='Sign In', command=click)

l_input_username.grid(row=0, column=0, sticky='n', padx=60, pady=10)
l_username.grid(row=1, column=0, sticky='n', padx=60, pady=2)
l_input_password.grid(row=2, column=0, sticky='n', padx=60, pady=10)
l_password.grid(row=3, column=0, sticky='n', padx=60, pady=2)
l_input_database.grid(row=4, column=0, sticky='n', padx=60, pady=10)
l_database.grid(row=5, column=0, sticky='n', padx=60, pady=2)
l_sign_in.grid(row=6, column=0, sticky='n', padx=60, pady=20)

authorization_window.mainloop()
