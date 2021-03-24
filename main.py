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
    global notebookTab1,notebookTab2
    notebookTab1 = ttk.Frame(notebook)
    notebookTab1.identifier = "search" # An Identifier to distinguish later in the program between the parents
    create_lookup(notebookTab1)
    notebook.add(notebookTab1, text='Data Lookup')
    notebookTab2 = ttk.Frame(notebook)
    notebookTab2.identifier = "modify"
    create_lookup(notebookTab2)
    notebook.add(notebookTab2, text='Modify Data')
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
    global fields
    tables = tables_in_sqlite_db(con)
    if master.identifier == 'search':
        tables.insert(0,'All')
    else:
        pass
    fields = []
    table_lbl = ttk.Label(master,text='Table:')
    table_lbl.grid(row=0,column=0,pady=10)
    field_lbl = ttk.Label(master,text='Field:')
    field_lbl.grid(row=0,column=2,pady=10)
    field_txt = tk.StringVar()
    table_txt = tk.StringVar()
    table_combo = ttk.Combobox(master,textvariable=table_txt,values=tables,state='readonly')
    table_combo.grid(row=0,column=1,pady=10)
    field_combo = ttk.Combobox(master,textvariable=field_txt,values=fields,state='readonly',postcommand=lambda :get_fields(cur,field_combo,tables,table_txt))
    field_combo.grid(row=0,column=3,pady=10)
    query_lbl = ttk.Label(master,text='Search Query:')
    query_lbl.grid(row=0,column=4,pady=10)
    query_txt = tk.StringVar()
    query_ent = ttk.Entry(master,textvariable=query_txt)
    query_ent.bind("<Return>",lambda e: display_lookup(master,tables,field_txt,table_txt,query_txt))
    query_ent.grid(row=0,column=5,pady=10)
    go_btn = ttk.Button(master,text='Go',command=lambda : display_lookup(master,tables,field_txt,table_txt,query_txt))
    go_btn.grid(row=0,column=6,pady=10)
    sep = ttk.Separator(master,orient='horizontal')
    sep.grid(row=1,column=0,columnspan=7,sticky='nsew')
    if master.identifier == 'search':
        copy_btn = ttk.Button(master,text='Copy',command=lambda : item_selected())
    elif master.identifier == 'modify':
        copy_btn = ttk.Button(master,text='Modify',command= lambda : modify(fields,con,cur,table_txt))
    copy_btn.grid(row=3,column=0,columnspan=7)

def get_fields(cur,combo,tables,table_txt):
    """To Get Fields According to the Table

    Args:
        cur (sqlite.Cursor): Cursor object
        combo (ttk.Combobox): Combobox object
        tables (list): List of all queries in the database
        table_txt (StringVar): String Varible of the Table Name Selected
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

def display_lookup(master,tables,field_txt,table_txt,query_txt):
    """To Display Treeview of the Data

    Args:
        master (ttk.Frame): Frame to pack the widget in
        tables (List): List of all queries in the database
        field_txt (StringVar): String Variable of the field
        table_txt (StringVar): String Varibale of the Table
        query_txt (StringVar): String Variable of the Query
    """
    global tree
    tree = ttk.Treeview(master, columns=fields, show='headings')
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
    try:
        if tree.selection()==():
            showerror('Error','No Data Selected!')
            return
    except NameError:
        showerror('Error','No Data Selected!')
        return
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

def modify(fields,con,cur,table_txt):
    """To Create TopLevel and Widgets for the modification of values

    Args:
        fields (list): List of all the columns in the query
        con (sqlite3.connect): SQLite Connection Object
        cur (sqlite3.cursor): Cursor Object
        table_txt (StringVar): String Variable of the Table Selected
    """
    try:
        selected_item = tree.item(tree.selection()[0])['values']
    except (IndexError,NameError):
        showerror('Error','No Data Selected!')
    modify_top = tk.Toplevel(root)  # TopLevel to show Label and Entries to allow changes
    modify_top.focus_set()
    modify_top.title('Modify Data')
    modify_top.resizable(0,0)
    modify_top.configure(bg='white')
    windowWidth=280
    windowHeight=250
    xCordinate,yCordinate = calc_location(windowWidth,windowHeight)
    modify_top.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, xCordinate, yCordinate))
    global stringvar_list
    stringvar_list = [tk.StringVar() for s in range(len(selected_item))]    # List of String Variables to store the text variables of the entries
    for var in range(len(stringvar_list)):
        stringvar_list[var].set(selected_item[var])     # Setting old values to the String Variables
    row = 0
    col = 0
    frm = ttk.Frame(modify_top)
    for i in range(len(fields[1:])):
        lbl = ttk.Label(frm,text=fields[1:][i])
        ent = ttk.Entry(frm,textvariable=stringvar_list[1:][i])
        lbl.grid(row=row,column=col,padx=2,pady=2)
        ent.grid(row=row,column=col+1,padx=2,pady=2)
        row+=1
    frm.grid(sticky='nsew',row=0,column=0,padx=30,pady=20)
    make_changes_btn = ttk.Button(modify_top,text='Make Changes',command = lambda : change(modify_top,con,cur,table_txt,fields,stringvar_list))
    modify_top.bind("<Return>",lambda e: change(modify_top,con,cur,table_txt,fields,stringvar_list))
    make_changes_btn.grid(row=1,column=0)

def change(modify_top,con,cur,table_txt,fields,stringvar_list):
    """To Modify the Values

    Args:
        modify_top (TopLevel): TopLevel which will be destoyed after making changes.
        con (sqlite3.connect): SQLite Connection Object
        cur (sqlite3.cursor): SQLite Cursor Object
        table_txt (StringVar): String Variable of the Table Selected
        fields (List): List of all the fields in the query
        stringvar_list (StringVar list[]): List of String Variables containing the changed or unchanged values
    """
    update_sql = []
    for i in range(len(fields[1:])):
        update_sql.append(f"{fields[1:][i]} = '{stringvar_list[1:][i].get()}'")
    sql = ','.join(update_sql)
    sql = f"UPDATE {table_txt.get()} SET {sql} WHERE {fields[0]}='{stringvar_list[0].get()}'"
    cur.execute(sql)
    con.commit()
    showinfo('Successful','Data Modification Successful!')
    edit(stringvar_list)
    modify_top.destroy()

def edit(stringvar_list):
    """To change old values in the TreeView with the New Values

    Args:
        stringvar_list (StringVar list[]): List of String Variables containing changed or unchanged values
    """
    x = tree.get_children()
    string_list = tuple(var.get() for var in stringvar_list)
    for item in x:
        if item==tree.selection()[0]:
            tree.item(item,values=string_list)


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