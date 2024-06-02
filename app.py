import os

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from xmlhandler import XMLHandler

xmlh : XMLHandler = None

def loadfile():
    xmlh = XMLHandler(filepath=pathvariable.get())
    xmlh.loadfile()
    print(xmlh)
    renderTable(mainframe, data=xmlh.allElements)

def _notImplemented():
    print("not implemented")
    pass

def callVersionWindow():
    messagebox.showinfo("Version","running on Version 1")

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

def setPassword():
    pass

def renderTable(master, data:dict={}):
    # render header
    borderwith : int = 2
    borderstyle : str = "ridge"
    tk.Label(master, text="[]", borderwidth=borderwith, relief=borderstyle).grid(row=1, column=1)
    tk.Label(master, text="ID", borderwidth=borderwith, relief=borderstyle).grid(row=1, column=2)
    tk.Label(master, text="Displayname", borderwidth=borderwith, relief=borderstyle).grid(row=1, column=3)
    tk.Label(master, text="User", borderwidth=borderwith, relief=borderstyle).grid(row=1, column=4)
    tk.Label(master, text="Password", borderwidth=borderwith, relief=borderstyle).grid(row=1, column=5)
    if len(data) == 0: return


    for row, key in enumerate(data.keys(), start=2):
        selectbutton = tk.Checkbutton(master, borderwidth=borderwith, relief=borderstyle)

        #selectbutton = ttk.Checkbutton(master)
        #selectbutton.configure(borderwith=borderwith)
        #selectbutton.state(['!alternate']) # init with option disabled
        selectbutton.grid(row=row, column=1)
        tk.Label(master, text=key, borderwidth=borderwith, relief=borderstyle).grid(row=row, column=2)
        tk.Label(master, text=data[key]['name'], borderwidth=borderwith, relief=borderstyle).grid(row=row, column=3)
        tk.Label(master, text=data[key]['user'], borderwidth=borderwith, relief=borderstyle).grid(row=row, column=4)
        tk.Label(master, text=data[key]['password'], borderwidth=borderwith, relief=borderstyle).grid(row=row, column=5)


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
filemenu.add_command(label="Exit", command=root.quit)

# Menu: Auswahl
selectionmenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Auswahl", menu=selectionmenu)
selectionmenu.add_command(label="Alles auswählen", command=_notImplemented)
selectionmenu.add_command(label="Alles abwählen", command=_notImplemented)
selectionmenu.add_command(label="Auswahl umkehren", command=_notImplemented)

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
pathinput = ttk.Entry(pathframe, textvariable=pathvariable)
pathinput.pack(side=tk.RIGHT, expand=True, fill='x', padx=5)

#ttk.Separator(root).pack(side=tk.TOP, fill='x', padx=0, pady=5)
# Options-Frame
optionsframe = tk.Frame(root, pady=5, padx=5)
optionsframe.pack(side=tk.TOP, fill='x')

loadbutton = ttk.Button(optionsframe, command=loadfile)
loadbutton.configure(text="Laden")
loadbutton.pack(side=tk.LEFT)

savebutton = ttk.Button(optionsframe)
savebutton.configure(text="Speichern")
savebutton.pack(side=tk.LEFT)

showPassword = ttk.Checkbutton(optionsframe)
showPassword.configure(text="zeige Password")
showPassword.state(['!alternate']) # init with option disabled
showPassword.pack(side=tk.RIGHT)

# Main-Frame
mainframe = tk.Frame(root, padx=5, pady=5)
mainframe.pack(side=tk.TOP, fill='both')

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

userbutton = ttk.Button(actionframe)
userbutton.configure(text="setze User",padding=5)
userbutton.pack(side=tk.LEFT, padx=5)

passwordbutton = ttk.Button(actionframe)
passwordbutton.configure(text="setze Password", padding=5)
passwordbutton.pack(side=tk.LEFT, padx=5)

ttk.Separator(root).pack(side=tk.BOTTOM, expand=False, fill='x', pady=2)

root.mainloop()
