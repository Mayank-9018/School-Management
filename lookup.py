import sqlite3
from tkinter.messagebox import showerror

con = sqlite3.connect('data.db')
cur = con.cursor()

def search(table,field,value,tables):
    """To Search for Data in the Database

    Args:
        table (String): Name of the table to search from
        field (String): Name of the field to search from
        value (String): Value to search for
        tables (list): List of all the tables in the database

    Returns:
        Cursor: Cursor of the search results
    """
    if not value.strip()=='':
        new_val = '%'+value+'%'
    else:
        new_val = '%'
    if not field=='':
        if not table=='All':
            sql = f"SELECT * from {table} WHERE {field} LIKE '{new_val}'"
        else:
            select_sql = tuple(f"Select * from {t} WHERE {field} LIKE '{new_val}'" for t in tables[1:])
            sql = ' UNION ALL '.join(select_sql)
        h = cur.execute(sql)
        return h
    else:
        showerror(title='Field Error',message='Field Cannot be empty.')
        return ()
