import tkinter as tk
from tkinter import ttk
import base64

def get_cred():
    ''' To create a Toplevel window to get Credentials from the user '''
    global cred_win
    cred_win = tk.Toplevel()
    cred_win.title('Login')
    cred_win.resizable(0,0)
    cred_win.bind("<Return>",validate_cred)
    cred_win.configure(bg='white')
    windowWidth = 280
    windowHeight = 170
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    xCordinate = int((screenWidth/2) - (windowWidth/2))
    yCordinate = int((screenHeight/2) - (windowHeight/2))
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
    ''' To Validate Credentials entered by the user.
    The setting.management file contains the passwords in base64 encoded form.
    Not to implement security but to fake it '''
    with open('setting.management','r') as fhand:
        user = base64.b64decode(bytes(fhand.readline(),'utf-8')).decode()
        passw = base64.b64decode(bytes(fhand.readline(),'utf-8')).decode()
        if user==username.get().strip() and passw==password.get().strip():
            error_lbl['foreground'] = 'green'   # Showing Success Message
            error.set('\u2713 Login Successful')
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
    notebookTab1 = ttk.Frame(notebook)
    insert_scrollbar(notebookTab1)
    notebook.add(notebookTab1, text='Data Lookup')
    notebookTab2 = ttk.Frame(notebook)
    insert_scrollbar(notebookTab2)
    notebook.add(notebookTab2, text='Student Details')
    notebookTab3 = ttk.Frame(notebook)
    insert_scrollbar(notebookTab3)
    notebook.add(notebookTab3, text='Teacher Details')
    notebook.pack(fill='both',expand=1,padx=50,pady=50)

def insert_scrollbar(tab):
    '''
    To insert scrollbar to various tabs of the notebook

    Args:
        tab (frame object): The Frame object in which scrollbar will be added'''
    canvas = tk.Canvas(tab, borderwidth=0)
    canvas.bind_all("<MouseWheel>", lambda event: on_mousewheel(event,canvas))
    frame = tk.Frame(canvas,bd=0)
    vsb = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((4,4), window=frame, anchor="nw")
    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

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
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
xCordinate = int((screenWidth/2) - (windowWidth/2))
yCordinate = int((screenHeight/2) - (windowHeight/2))
root.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, xCordinate, yCordinate))
login_btn = ttk.Button(root,text="Login",command=get_cred)
login_btn.pack(expand=1)
root.mainloop()