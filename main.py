from tables import tables_in_sqlite_db
import tkinter as tk
from tkinter import ttk
from validate import validate
import sqlite3
from lookup import search
from tkinter.messagebox import showerror, showinfo
import json

def calc_location(windowWidth,windowHeight):
    """To Calculate location to place the window

    Args:
        windowWidth (int): Desired Width of the Window
        windowHeight (int): Desired Height of the Window

    Returns:
        xCordinate,YCordinate: X and Y Coordinates
    """
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    xCordinate = int((screenWidth/2) - (windowWidth/2))
    yCordinate = int((screenHeight/2) - (windowHeight/2))
    return xCordinate,yCordinate

def get_cred():
    ''' To create a Toplevel window to get Credentials from the user '''
    global cred_win
    cred_win = tk.Toplevel()
    cred_win.focus_set()
    cred_win.title('Login')
    cred_win.resizable(0,0)
    cred_win.bind("<Return>",validate_cred)
    cred_win.configure(bg='white')
    windowWidth=280
    windowHeight=170
    xCordinate,yCordinate = calc_location(windowWidth,windowHeight)
    cred_win.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, xCordinate, yCordinate))
    user_lbl = ttk.Label(cred_win,text='Username:')
    user_ent = ttk.Entry(cred_win,textvariable=username)
    pass_lbl = ttk.Label(cred_win,text='Password:')
    pass_ent = ttk.Entry(cred_win,show='•',textvariable=password)
    login_btn = ttk.Button(cred_win,text='Login')
    login_btn.bind("<Button-1>",validate_cred)
    global error_lbl
    error_lbl = ttk.Label(cred_win,textvariable=error,foreground='red')
    user_lbl.place(x=40,y=30)
    user_ent.place(x=110,y=30)
    pass_lbl.place(x=40,y=60)
    pass_ent.place(x=110,y=60)
    login_btn.place(x=110,y=120)
    error_lbl.place(x=95,y=90)
    cred_win.mainloop()

def validate_cred(event):
    """To Validate Credentials entered by the User

    Args:
        event (event): event object
    """
    if validate(username.get(),password.get()):
        error_lbl['foreground'] = 'green'   # Showing Success Message
        error.set('\u2713 Login Successful')
        cred_win.update()
        create_window() #Creating the windows with other functionalities
        cred_win.destroy()  # Destroying the Toplevel created to get credentials
    else:
        username.set('')
        password.set('')
        error.set('\u2757 Wrong Credentials')

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_mousewheel(event,canvas):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")


def create_window():
    '''To Construct the Window'''
    login_btn.pack_forget() # Removing the Login Button
    notebook = ttk.Notebook(root)
    global notebookTab1
    notebookTab1 = ttk.Frame(notebook)
    create_lookup(notebookTab1)
    notebook.add(notebookTab1, text='Data Lookup')
    notebookTab2 = ttk.Frame(notebook)
    notebook.add(notebookTab2, text='Student Details')
    notebookTab3 = ttk.Frame(notebook)
    notebook.add(notebookTab3, text='Teacher Details')
    notebook.pack(fill='both',expand=1,padx=50,pady=50)


def create_lookup(master):
    """To create widgets for the lookup notebook

    Args:
        master (ttk.Frame): Frame to pack the widgets in
    """
    master.rowconfigure([0,1,3],weight=1)
    master.rowconfigure([2],weight=6)
    master.columnconfigure([0,1,2,3,4,5,6],weight=1)
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    global fields,tables
    tables = tables_in_sqlite_db(con)
    tables.insert(0,'All')
    fields = []
    table_lbl = ttk.Label(master,text='Table:')
    table_lbl.grid(row=0,column=0,padx=10,pady=10)
    field_lbl = ttk.Label(master,text='Field:')
    field_lbl.grid(row=0,column=2,padx=10,pady=10)
    global field_txt,table_txt
    field_txt = tk.StringVar()
    table_txt = tk.StringVar()
    table_combo = ttk.Combobox(master,textvariable=table_txt,values=tables,state='readonly')
    table_combo.grid(row=0,column=1,padx=10,pady=10)
    field_combo = ttk.Combobox(master,textvariable=field_txt,values=fields,state='readonly',postcommand=lambda :get_fields(cur,field_combo))
    field_combo.grid(row=0,column=3,padx=10,pady=10)
    query_lbl = ttk.Label(master,text='Search Query:')
    query_lbl.grid(row=0,column=4,padx=10,pady=10)
    global query_txt
    query_txt = tk.StringVar()
    query_ent = ttk.Entry(master,textvariable=query_txt)
    query_ent.bind("<Return>",lambda e: display_lookup())
    query_ent.grid(row=0,column=5,padx=10,pady=10)
    go_btn = ttk.Button(master,text='Go',command=display_lookup)
    go_btn.grid(row=0,column=6,padx=10,pady=10)
    sep = ttk.Separator(master,orient='horizontal')
    sep.grid(row=1,column=0,columnspan=7,sticky='nsew')
    copy_btn = ttk.Button(notebookTab1,text='Copy',command=item_selected)
    copy_btn.grid(row=3,column=0,columnspan=7)

def get_fields(cur,combo):
    """To Get Fields According to the Table

    Args:
        cur (sqlite.Cursor): Cursor object
        combo (ttk.Combobox): Combobox object
    """
    select_sql = tuple(f'Select * from {t}' for t in tables[1:])
    if table_txt.get()=='':
        showerror('Table Error',message='Table Field cannot be empty.')
        return
    if table_txt.get()=='All':
        sql = ' UNION ALL '.join(select_sql)
    else:
        sql = f'SELECT * from {table_txt.get()}'
    cursor = cur.execute(sql)
    global fields
    fields = [i[0] for i in cursor.description]
    combo['values'] = fields

def display_lookup():
    """To Display Treeview of the Data
    """
    global tree
    tree = ttk.Treeview(notebookTab1, columns=fields, show='headings')
    tree.grid(row=2,column=0,columnspan=7,sticky='nsew')
    for item in fields:
        tree.heading(item, text=item.capitalize())
    for item in search(table_txt.get(),field_txt.get(),query_txt.get(),tables):
        tree.insert('', tk.END, values=item)

def item_selected():
    """Triggered when the user clicks the Copy Button; Copies the JSON of the selected data to the clipboard
    """
    dic = {}
    dic_list = []
    for selected_item in tree.selection():
        inner_dic = {}
        item = tree.item(selected_item)
        record = item['values']
        for i in range(len(fields)):
            inner_dic[fields[i]] = record[i]
        dic_list.append(inner_dic)
    dic['student'] = dic_list
    json_out = json.dumps(dic,indent=4)
    root.clipboard_clear()
    root.clipboard_append(json_out)
    showinfo(title='Information',
            message='JSON Copied to Clipboard!')

root = tk.Tk()
root.configure(background='white')
style = ttk.Style(root)
style.configure('.',background='white')
username = tk.StringVar()
password = tk.StringVar()
error = tk.StringVar()
root.title('School Management')
windowWidth = 800
windowHeight = 530
xCordinate,yCordinate = calc_location(windowWidth,windowHeight)
root.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, xCordinate, yCordinate))
login_btn = ttk.Button(root,text="Login",command=get_cred)
login_btn.pack(expand=1)
root.mainloop()