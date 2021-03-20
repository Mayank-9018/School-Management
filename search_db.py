import sqlite3

def search(database,table,search_query):
    database = 'data.db'
    con = sqlite3.connect(database)
    cur = con.cursor()
    search_result = cur.execute(f'SELECT * from {table} WHERE name = ?',(search_query,))
    for (name,phone) in search_result:
        print(name,phone)

def add(database,table,namee,phonee):
    con = sqlite3.connect(database)
    cur = con.cursor()
    add = cur.execute(f'INSERT INTO {table}(name,phone) VALUES (?,?)',(namee,phonee))
    con.commit()
    new_l = cur.execute(f'SELECT * from {table}')
    for item in new_l:
        print(item)

def delete(database,table,namee):
    con = sqlite3.connect(database)
    cur = con.cursor()
    delete = cur.execute(f'DELETE FROM {table} WHERE name = ?',(namee,))
    con.commit()
    new_l = cur.execute(f'SELECT * from {table}')
    for item in new_l:
        print(item)

# search('data.db','Teachers','Harsh')
# add('data.db','Teachers','Harsh',9695445538)
# delete('data.db','Students','Harsh')