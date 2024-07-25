from tkinter import *
from tkinter import filedialog, messagebox
import subprocess
import os

path = ''
temp_file = 'temp_script.py'

def font_inc(event=None):
    global font_size
    font_size += 1
    textarea.config(font=('arial', font_size, 'bold'))

def font_dec(event=None):
    global font_size
    font_size -= 1
    textarea.config(font=('arial', font_size, 'bold'))

def run_code():
    global temp_file
    with open(temp_file, 'w') as file:
        file.write(textarea.get(1.0, END))
    command = f'python {temp_file}'
    run_file = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = run_file.communicate()
    outputarea.delete(1.0, END)
    outputarea.insert(1.0, output.decode('utf-8'))
    outputarea.insert(1.0, error.decode('utf-8'))

def saveas(event=None):
    global path
    path = filedialog.asksaveasfilename(filetypes=[('Python Files', '*.py')], defaultextension=('.py'))
    if path != '':
        with open(path, 'w') as file:
            file.write(textarea.get(1.0, END))

def openfile(event=None):
    global path
    path = filedialog.askopenfilename(filetypes=[('Python Files', '*.py')], defaultextension=('.py'))
    if path != '':
        with open(path, 'r') as file:
            data = file.read()
            textarea.delete(1.0, END)
            textarea.insert(1.0, data)

def save(event=None):
    if path == '':
        saveas()
    else:
        with open(path, 'w') as file:
            file.write(textarea.get(1.0, END))

def new(event=None):
    global path
    path = ''
    textarea.delete(1.0, END)
    outputarea.delete(1.0, END)

def iexit(event=None):
    result = messagebox.askyesno('Confirm', 'Do you want to exit?')
    if result:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        root.destroy()

def theme():
    if check.get() == 'light':
        textarea.config(bg='white', fg='black')
        outputarea.config(bg='white', fg='black')
    if check.get() == 'dark':
        textarea.config(bg='black', fg='white')
        outputarea.config(bg='black', fg='white')

def clear():
    textarea.delete(1.0, END)
    outputarea.delete(1.0, END)

font_size = 18

root = Tk()
root.geometry('1270x670+0+0')
root.title('Python Editor created by Hema')
check = StringVar()
check.set('light')
myMenu = Menu()

filemenu = Menu(myMenu, tearoff=False)
filemenu.add_command(label='New File', accelerator='Ctrl+N', command=new)
filemenu.add_command(label='Open File', accelerator='Ctrl+O', command=openfile)
filemenu.add_command(label='Save', accelerator='Ctrl+S', command=save)
filemenu.add_command(label='Save as', accelerator='Ctrl+Shift+S', command=saveas)
filemenu.add_command(label='Exit', accelerator='Ctrl+Q', command=iexit)
myMenu.add_cascade(label='File', menu=filemenu)

thememenu = Menu(myMenu, tearoff=False)
thememenu.add_radiobutton(label='Light', variable=check, value='light', command=theme)
thememenu.add_radiobutton(label='Dark', variable=check, value='dark', command=theme)
myMenu.add_cascade(label='Themes', menu=thememenu)

myMenu.add_command(label='Clear', command=clear)
myMenu.add_command(label='Run', command=run_code)

editFrame = Frame(root, bg='white')
editFrame.place(x=0, y=0, height=500, relwidth=1)

scrollbar = Scrollbar(editFrame, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=Y)
textarea = Text(editFrame, font=('arial', font_size, 'bold'), yscrollcommand=scrollbar.set)
textarea.pack(fill=BOTH)
scrollbar.config(command=textarea.yview)

outputFrame = LabelFrame(root, text='Output', font=('arial', 12, 'bold'))
outputFrame.place(x=0, y=500, relwidth=1, height=170)

scrollbar1 = Scrollbar(outputFrame, orient=VERTICAL)
scrollbar1.pack(side=RIGHT, fill=Y)
outputarea = Text(outputFrame, font=('arial', font_size, 'bold'), yscrollcommand=scrollbar1.set)
outputarea.pack(fill=BOTH)
scrollbar1.config(command=outputarea.yview)

root.config(menu=myMenu)

root.bind('<Control-n>', new)
root.bind('<Control-o>', openfile)
root.bind('<Control-s>', save)
root.bind('<Control-Shift-s>', saveas)
root.bind('<Control-q>', iexit)
root.bind('<Control-+>', font_inc)
root.bind('<Control-m>', font_dec)
root.mainloop()
