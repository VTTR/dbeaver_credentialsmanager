import os
if os.name == 'nt':
    from ctypes import windll  # Only exists on Windows.

import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import ttk
import webbrowser

from xmlhandler import XMLHandler
from dbeavercrypto import decrypt, encrypt

xmlh: XMLHandler = XMLHandler()
somethingHasChangedFlag: bool = False

def loadfile():
    xmlh.setPath(pathvariable.get())
    xmlh.loadfile()
    renderTable(mainframe)


def savefile():
    xmlh.savefile()
    global somethingHasChangedFlag
    somethingHasChangedFlag = False


def openRepositoryInBrowser():
    webbrowser.open_new("https://github.com/VTTR/dbeaver_credentialsmanager")


def openFileSelector():
    path = filedialog.askopenfile(
        title="Open file",
        filetypes=(
            ("XML files", "*.xml"),
            ("all fFiles", "*.*")
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


def autodetect() -> str:
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
    global somethingHasChangedFlag
    somethingHasChangedFlag = True
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
    global somethingHasChangedFlag
    somethingHasChangedFlag = True
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


def exitApplication() -> None:
    print("Exiting Application")

    if not somethingHasChangedFlag:
        return root.destroy()

    saverequested: bool = messagebox.askyesnocancel("Exit", "Some changes hasn't been saved. Do you want to save before exiting?")
    if saverequested:
        savefile()
        root.destroy()
    elif saverequested is None:
        return
    elif not saverequested:
        root.destroy()


root = tk.Tk()
root.title("DBeaver Credentialsmanager")
root.geometry("900x500")
root.minsize(900, 500)
root.protocol('WM_DELETE_WINDOW', exitApplication)

# icon
if os.name == 'nt':
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

# menu: file
filemenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open file..", command=openFileSelector)
filemenu.add_command(label="Exit", command=exitApplication)

# menu: selection
selectionmenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Selection", menu=selectionmenu)
selectionmenu.add_command(label="Select all", command=selectAll)
selectionmenu.add_command(label="Deselect all", command=deselectAll)
selectionmenu.add_command(label="Invert selection", command=invertSelection)

# menu: about
menu.add_command(label="About", command=openRepositoryInBrowser)

# menu: exit
menu.add_command(label="Exit", command=exitApplication)

# path-frame
pathframe = tk.Frame(root, pady=5, padx=5)
pathframe.pack(side=tk.TOP, fill='x')

autodetectbutton = ttk.Button(pathframe)
autodetectbutton.configure(text="auto-detect", command=lambda: pathvariable.set(autodetect()))
autodetectbutton.pack(side=tk.LEFT, padx=5)

pathvariable = tk.StringVar()
pathinput = ttk.Entry(pathframe, textvariable=pathvariable, validate='focusin', validatecommand=openFileSelector)
pathinput.pack(side=tk.RIGHT, expand=True, fill='x', padx=5)

# options-frame
optionsframe = tk.Frame(root, pady=5, padx=5)
optionsframe.pack(side=tk.TOP, fill='x')

loadbutton = ttk.Button(optionsframe, command=loadfile)
loadbutton.configure(text="load")
loadbutton.pack(side=tk.LEFT)

savebutton = ttk.Button(optionsframe, command=savefile)
savebutton.configure(text="save")
savebutton.pack(side=tk.LEFT)

showPasswordValue = tk.IntVar()
showPassword = ttk.Checkbutton(optionsframe, command=togglePasswordVisibility)
showPassword.configure(text="display password")
showPassword.state(['!alternate']) # init with option disabled
showPassword.pack(side=tk.RIGHT)

# main-frame
mainframe = tk.Frame(root, padx=5, pady=5)
mainframe.pack(side=tk.TOP, fill='both', expand=True)
renderTable(mainframe)

# footer-frame
footerframe = tk.Frame(root)
footerframe.pack(side=tk.BOTTOM, fill='x')
ttk.Separator(footerframe).pack(side=tk.TOP, expand=True, fill='x', pady=10)
ttk.Label(footerframe, text="© Fabian Vetter (2024)").place(relx=0.5, rely=0.6, anchor=tk.CENTER)
ttk.Sizegrip(footerframe).pack(side=tk.RIGHT)

# action-frame
actionframe = tk.Frame(root, padx=5, pady=2)
actionframe.pack(side=tk.BOTTOM, fill='x')

userbutton = ttk.Button(actionframe, command=setNewUser)
userbutton.configure(text="set user", padding=5)
userbutton.pack(side=tk.LEFT, padx=5)

passwordbutton = ttk.Button(actionframe, command=setNewPassword)
passwordbutton.configure(text="set password", padding=5)
passwordbutton.pack(side=tk.LEFT, padx=5)

renderDBeaverRunningWarning()

# disable action buttons in case of a running dbeaver instance
if isDBeaverRunning():
    userbutton.state(["disabled"])
    passwordbutton.state(["disabled"])

ttk.Separator(root).pack(side=tk.BOTTOM, expand=False, fill='x', pady=2)

root.mainloop()
