import tkinter as tk
from tkinter import Canvas, Frame, Grid, PhotoImage, ttk
import base64
from time import sleep
from typing import Text

def get_cred():
    global cred_win
    cred_win = tk.Toplevel()
    cred_win.title('Login')
    cred_win.resizable(0,0)
    cred_win.bind("<Return>",validate_cred)
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
    login_btn = ttk.Button(cred_win,text='Login',style='AccentButton')
    login_btn.bind("<Button-1>",validate_cred)
    global error_lbl
    error_lbl = ttk.Label(cred_win,textvariable=error,foreground='red')
    user_lbl.place(x=40,y=30)
    user_ent.place(x=110,y=25)
    pass_lbl.place(x=40,y=70)
    pass_ent.place(x=110,y=60)
    login_btn.place(x=110,y=120)
    error_lbl.place(x=95,y=96)
    cred_win.mainloop()

def validate_cred(event):
    with open('setting.management','r') as fhand:
        user = base64.b64decode(bytes(fhand.readline(),'utf-8')).decode()
        passw = base64.b64decode(bytes(fhand.readline(),'utf-8')).decode()
        if user==username.get().strip() and passw==password.get().strip():
            error_lbl['foreground'] = 'green'
            error.set('\u2713 Login Successful')
            cred_win.update()
            create_window()
            cred_win.destroy()
        else:
            username.set('')
            password.set('')
            error.set('\u2757 Wrong Credentials')

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

def create_window():
    login_btn.pack_forget()
    notebook = ttk.Notebook(root)
    notebookTab1 = ttk.Frame(notebook)
    global canvas
    canvas = tk.Canvas(notebookTab1, borderwidth=0)
    canvas.bind_all("<MouseWheel>", on_mousewheel)
    frame = tk.Frame(canvas)
    for _ in range(50):
        text = ttk.Entry(frame).pack()
    vsb = ttk.Scrollbar(notebookTab1, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((4,4), window=frame, anchor="nw")
    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
    notebook.add(notebookTab1, text='Data Lookup')
    notebookTab2 = ttk.Frame(notebook)
    notebook.add(notebookTab2, text='Student Details')
    notebookTab3 = ttk.Frame(notebook)
    notebook.add(notebookTab3, text='Teacher Details')
    notebook.pack(fill='both',expand=1,padx=50,pady=50)

def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def switch_theme():
    if light_style.theme_use()=='azure':
            dark_style.theme_use('azure-dark')
            root.configure(background='#333333')
            try:
                cred_win.configure(background='#333333')
            except:
                pass
    else:
            dark_style.theme_use('azure')
            root.configure(background='white')
            try:
                cred_win.configure(background='white')
            except:
                pass


root = tk.Tk()
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
light_style = ttk.Style(root)
dark_style = ttk.Style(root)
root.tk.call('source', r'Azure-ttk-theme\azure-dark.tcl')
root.tk.call('source', r'Azure-ttk-theme\azure.tcl')
light_style.theme_use('azure')
outer_frame = ttk.Frame(root)
login_btn = ttk.Button(root,text="Login",command=get_cred)
login_btn.pack(expand=1)
fking_btn = ttk.Button(root,text="switch",command=switch_theme)
# fking_btn.pack()
# outer_frame.pack(expand=1)
root.mainloop()