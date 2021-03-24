import sqlite3
from tkinter.messagebox import showinfo

con = sqlite3.connect('data.db')
cur = con.cursor()

