import sqlite3
con = sqlite3.connect('data.db')
cur = con.cursor()

def search(field,value):
    new_val = '%'+value+'%'
    h = cur.execute(f"SELECT * from Students WHERE {field} LIKE ? UNION ALL SELECT * from Teachers WHERE {field} LIKE ?",(new_val,new_val))
    return h
