import os

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def _notImplemented():
    print("not implemented")
    pass

def callVersionWindow():
    messagebox.showinfo("Version","running on Version 1")

def setPassword():
    pass

root = tk.Tk()
root.title("DBeaver Credentialsmanager")
root.geometry("700x300")
root.minsize(700,300)
root.maxsize(900,800)

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
autodetectbutton.configure(text="Auto-Detect")
autodetectbutton.pack(side=tk.LEFT)

pathinput = ttk.Entry(pathframe)
pathinput.pack(side=tk.RIGHT, expand=True, fill='x', padx=5)

#ttk.Separator(root).pack(side=tk.TOP, fill='x', padx=0, pady=5)
# Options-Frame
optionsframe = tk.Frame(root, pady=5, padx=5)
optionsframe.pack(side=tk.TOP, fill='x')

loadbutton = ttk.Button(optionsframe)
loadbutton.configure(text="Laden")
loadbutton.pack(side=tk.LEFT)

savebutton = ttk.Button(optionsframe)
savebutton.configure(text="Speichern")
savebutton.pack(side=tk.LEFT)

showPassword = ttk.Checkbutton(optionsframe)
showPassword.configure(text="zeige Password")
showPassword.state(['!alternate']) # init with option disabled
showPassword.pack(side=tk.RIGHT)


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