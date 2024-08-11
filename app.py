import os
if os.name == 'nt': from ctypes import windll

import subprocess
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

def callAboutWindow():
    import webbrowser
    def callback(url: str):
        webbrowser.open_new(url)

    about_window = tk.Toplevel()
    about_window.title("About")
    # about_window.config(width=400, height=300)
    about_window.geometry("400x300")
    ttk.Button(about_window, text="close", command=about_window.destroy).pack(side=tk.BOTTOM)

    repolink = tk.Label(about_window, text="Github-Repository", fg="blue", cursor="hand2")
    repolink.pack()
    repolink.bind("<Button-1>", lambda e: callback("https://github.com/VTTR/dbeaver_credentialsmanager"))


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
        if not isinstance(tree, ttk.Treeview):
            continue
        tree.selection_set(tree.get_children())


def deselectAll():
    for tree in mainframe.winfo_children():
        if not isinstance(tree, ttk.Treeview):
            continue
        tree.selection_set()

def invertSelection():
    for tree in mainframe.winfo_children():
        if not isinstance(tree, ttk.Treeview):
            continue
        tree.selection_toggle(tree.get_children())

def togglePasswordVisibility():
    showPasswordValue.set(0 if showPasswordValue.get()==1 else 1)
    renderTable(mainframe)

def autodetect():
    print("autodetection started")
    possiblepaths = [
        r'C:/ProgramData/DBeaver/configuration/.dbeaver4/General/.dbeaver-data-sources.xml'
        ]
    for file in possiblepaths:
        if os.path.isfile(file):
            return file
    return "file not found"

def setNewPassword() -> None:
    newPassword: str = simpledialog.askstring("input", "new password", parent=root, show='' if showPasswordValue.get() == 1 else '*')
    print(f"setting new password {newPassword[0]}***")
    for tree in mainframe.winfo_children():
        if not isinstance(tree, ttk.Treeview):
            continue
        for itemid in tree.selection():
            dbeaverid = tree.item(itemid)['values'][-1]
            xmlh.setPassword(id=dbeaverid, newPassword=encrypt(newPassword))
    renderTable(mainframe)

def setNewUser() -> None:
    newUser: str = simpledialog.askstring("input", "new username", parent=root)
    print(f"setting new User: {newUser}")
    for tree in mainframe.winfo_children():
        if not isinstance(tree, ttk.Treeview):
            continue
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

    if len(xmlh) == 0:
        return

    for index, item in enumerate(xmlh.allElements, start=0):
        data = xmlh.allElements[item]
        table.insert(parent='', index=index, values=(
            data['name'],
            data['user'],
            data['password'] if showPasswordValue.get() == 0 else decrypt(data['password']),
            item
        ))

def isDBeaverRunning() -> bool:
    if os.name == 'nt':
        # thanks to https://stackoverflow.com/questions/77370805/using-python-subprocess-to-open-powershell-causes-encoding-errors-in-stdout
        # Save the current console output code page and switch to 65001 (UTF-8)
        previousCp = windll.kernel32.GetConsoleOutputCP()
        windll.kernel32.SetConsoleOutputCP(65001)

        processname: str = 'dbeaver.exe'
        call: str = f'TASKLIST /FI "imagename eq {processname}"'
        output: str = subprocess.check_output(call).decode('utf-8')

        # Restore the previous output console code page.
        windll.kernel32.SetConsoleOutputCP(previousCp)

        last_line: str = output.strip().split('\r\n')[-1]
        return last_line.lower().startswith(processname.lower())
    return False

def renderDBeaverRunningWarning() -> None:
    if not isDBeaverRunning():
        return
    warningtext = """WARNING: A RUNNING DBEAVER INSTANCE DETECTED
    started in readonly mode"""
    warninglabel = tk.Label(master=actionframe, text=warningtext, background='red')
    warninglabel.pack(side=tk.LEFT, fill='x', expand=True)


root = tk.Tk()
root.title("DBeaver Credentialsmanager")
root.geometry("900x500")
root.minsize(900,500)

# icon
if os.name == 'nt':
    from ctypes import windll  # Only exists on Windows.
    myappid = "vttr.dbeaver_credentialsmanager.1"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# style
if 'winnative' in ttk.Style().theme_names():
    ttk.Style().theme_use('winnative')
else:
    ttk.Style().theme_use('default')

img = tk.PhotoImage(file=f'{os.path.dirname(__file__)}/assets/icon.gif')
root.iconphoto(False, img, img)

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
aboutmenu.add_command(label="Über", command=callAboutWindow)

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
mainframe.pack(side=tk.TOP, fill='both', expand=True)
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

renderDBeaverRunningWarning()

# disable action buttons in case of a running dbeaver instance
if isDBeaverRunning():
    userbutton.state(["disabled"])
    passwordbutton.state(["disabled"])

ttk.Separator(root).pack(side=tk.BOTTOM, expand=False, fill='x', pady=2)

root.mainloop()
