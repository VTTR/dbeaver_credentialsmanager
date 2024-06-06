import os

import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import ttk

from xmlhandler import XMLHandler
from dbeavercrypto import decrypt, encrypt

xmlh : XMLHandler = XMLHandler()

def loadfile():
    xmlh.setPath(pathvariable.get())
    xmlh.loadfile()
    renderTable(mainframe)

def savefile():
    xmlh.savefile()

def _notImplemented():
    print("not implemented")
    pass

def callVersionWindow():
    messagebox.showinfo("Version","running on Version 1")

def openFileSelector():
    path = filedialog.askopenfile(
        title="Datei öffnen",
        filetypes=(
            ("XML-Files", "*.xml"),
            ("All-Files", "*.*")
        )
    ).name
    pathvariable.set(path)

def selectAll():
    for tree in mainframe.winfo_children():
        if not isinstance(tree, ttk.Treeview): continue
        tree.selection_set(tree.get_children())


def deselectAll():
    for tree in mainframe.winfo_children():
        if not isinstance(tree, ttk.Treeview): continue
        tree.selection_set()

def invertSelection():
    for tree in mainframe.winfo_children():
        if not isinstance(tree, ttk.Treeview): continue
        tree.selection_toggle(tree.get_children())

def togglePasswordVisibility():
    showPasswordValue.set(0 if showPasswordValue.get()==1 else 1)
    renderTable(mainframe)

def autodetect():
    print("autodetection started")
    possiblepaths = [
        '~/Library/DBeaverData/workspace6/General/.dbeaver/credentials-config.json',
        '~/.local/share/DBeaverData/workspace6/General/.dbeaver/credentials-config.json',
        '~/.local/share/.DBeaverData/workspace6/General/.dbeaver/credentials-config.json',
        '/home/fabian/privat/dbeaver_credentialsmanager/dbeaver-data-sources.xml',
        r'C:/ProgramData/DBeaver/configuration/.dbeaver4/General/.dbeaver-data-sources.xml',
        '~/AppData/Roaming/DBeaverData/workspace6/General/.dbeaver/credentials-config.json',
        ]
    for file in possiblepaths:
        if os.path.isfile(file):
            return file
    return "file not found"

def setNewPassword() -> None:
    newPassword: str = tk.simpledialog.askstring("input", "new password", parent=root, show='' if showPasswordValue.get() == 1 else '*')
    print(f"setting new password {newPassword[0]}***")
    for tree in mainframe.winfo_children():
        if not isinstance(tree, ttk.Treeview): continue
        for itemid in tree.selection():
            dbeaverid = tree.item(itemid)['values'][-1]
            xmlh.setPassword(id=dbeaverid, newPassword=encrypt(newPassword))
    renderTable(mainframe)

def setNewUser() -> None:
    newUser: str = tk.simpledialog.askstring("input", "new username", parent=root)
    print(f"setting new User: {newUser}")
    for tree in mainframe.winfo_children():
        if not isinstance(tree, ttk.Treeview): continue
        for itemid in tree.selection():
            dbeaverid = tree.item(itemid)['values'][-1]
            xmlh.setUser(id=dbeaverid, newUser=newUser)
    renderTable(mainframe)

def renderTable(master):
    # clearing
    for widget in master.winfo_children():
        widget.destroy()

    table = ttk.Treeview(master, selectmode='extended')
    table.pack(side='left', expand=True, fill='both')
    table['columns'] = ['displayname', 'user', 'password', 'id']
    table.heading('displayname', text="Displayname")
    table.heading('user', text="User")
    table.heading('password', text="Password")
    table.heading('id', text="ID")
    table['show'] = 'headings'

    if len(xmlh) == 0: return
    for index, item in enumerate(xmlh.allElements, start=0):
        data = xmlh.allElements[item]
        table.insert(parent='', index=index, values=(
            data['name'],
            data['user'],
            data['password'] if showPasswordValue.get() == 0 else decrypt(data['password']),
            item
        ))


root = tk.Tk()
root.title("DBeaver Credentialsmanager")
root.geometry("900x500")
root.minsize(900,500)
#root.maxsize(1200,800)

# style
if 'winnative' in ttk.Style().theme_names():
    ttk.Style().theme_use('winnative')
else:
    ttk.Style().theme_use('default')


# icon
#small_icon = tk.PhotoImage(file="icon-16.png")
#large_icon = tk.PhotoImage(file="icon-32.png")
#root.iconphoto(False, large_icon, small_icon)
#root.iconbitmap("icon.ico")
img = tk.PhotoImage(file='icon.gif')
root.tk.call('wm', 'iconphoto', root._w, img)
root.tk.call('wm', 'group', root._w, root._w)

menu = tk.Menu(root)
root.config(menu=menu)

# Menü: Datei
filemenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Datei", menu=filemenu)
filemenu.add_command(label="Datei öffnen..", command=openFileSelector)
filemenu.add_command(label="Exit", command=root.quit)

# Menu: Auswahl
selectionmenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Auswahl", menu=selectionmenu)
selectionmenu.add_command(label="Alles auswählen", command=selectAll)
selectionmenu.add_command(label="Alles abwählen", command=deselectAll)
selectionmenu.add_command(label="Auswahl umkehren", command=invertSelection)

# Menu: Über
aboutmenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Über", menu=aboutmenu)
aboutmenu.add_command(label="Version", command=callVersionWindow)
aboutmenu.add_command(label="Über", command=_notImplemented)

menu.add_command(label="Exit", command=root.quit)

# Pfad-Frame
pathframe = tk.Frame(root, pady=5, padx=5)
pathframe.pack(side=tk.TOP, fill='x')

autodetectbutton = ttk.Button(pathframe)
autodetectbutton.configure(text="Auto-Detect", command=lambda: pathvariable.set(autodetect()))
autodetectbutton.pack(side=tk.LEFT, padx=5)

pathvariable = tk.StringVar()
pathinput = ttk.Entry(pathframe, textvariable=pathvariable, validate='focusin', validatecommand=openFileSelector)
pathinput.pack(side=tk.RIGHT, expand=True, fill='x', padx=5)

#ttk.Separator(root).pack(side=tk.TOP, fill='x', padx=0, pady=5)
# Options-Frame
optionsframe = tk.Frame(root, pady=5, padx=5)
optionsframe.pack(side=tk.TOP, fill='x')

loadbutton = ttk.Button(optionsframe, command=loadfile)
loadbutton.configure(text="Laden")
loadbutton.pack(side=tk.LEFT)

savebutton = ttk.Button(optionsframe, command=savefile)
savebutton.configure(text="Speichern")
savebutton.pack(side=tk.LEFT)

showPasswordValue = tk.IntVar()
showPassword = ttk.Checkbutton(optionsframe, command=togglePasswordVisibility)
showPassword.configure(text="zeige Password")
showPassword.state(['!alternate']) # init with option disabled
showPassword.pack(side=tk.RIGHT)

# Main-Frame
mainframe = tk.Frame(root, padx=5, pady=5)
mainframe.pack(side=tk.TOP, fill='both')
renderTable(mainframe)

# Footer-Frame
footerframe = tk.Frame(root)
footerframe.pack(side=tk.BOTTOM, fill='x')
ttk.Separator(footerframe).pack(side=tk.TOP, expand=True, fill='x', pady=10)
#ttk.Label(footerframe, text="© Fabian Vetter (2024)").pack(side=tk.LEFT)
ttk.Label(footerframe, text="© Fabian Vetter (2024)").place(relx=0.5, rely=0.6, anchor=tk.CENTER)
ttk.Sizegrip(footerframe).pack(side=tk.RIGHT)

# Action-Frame
actionframe = tk.Frame(root, padx=5, pady=2)
actionframe.pack(side=tk.BOTTOM, fill='x')

userbutton = ttk.Button(actionframe, command=setNewUser)
userbutton.configure(text="setze User",padding=5)
userbutton.pack(side=tk.LEFT, padx=5)

passwordbutton = ttk.Button(actionframe, command=setNewPassword)
passwordbutton.configure(text="setze Password", padding=5)
passwordbutton.pack(side=tk.LEFT, padx=5)

ttk.Separator(root).pack(side=tk.BOTTOM, expand=False, fill='x', pady=2)

root.mainloop()
