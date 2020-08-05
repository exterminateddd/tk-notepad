import json
import tkinter

from tkinter import *


def edit_note(name: str):
    note_edit = Tk()
    note_edit.title('Изменение: '+name)
    note_edit.geometry('600x480')
    note_edit.resizable(False, False)

    exit_button = Button(note_edit)
    exit_button.place(width=80, height=30)
    exit_button.configure(text='Выйти', command=lambda: note_edit.destroy())
    exit_button.pack(anchor="nw")

    edit_success = Label(note_edit)
    edit_success.configure(background="green", foreground="white")
    edit_success.place(x=0, y=250)

    def set_note():
        with open('notes.json', "r") as f:
            notes = json.load(f)
        notes[name] = edit_area.get("0.1", END)
        with open('notes.json', "w") as f:
            json.dump(notes, f, indent=4)
        edit_success.place_forget()
        edit_success.configure(text="Сохранено")
        edit_success.place(x=0, y=306)

    edit_area = Text(note_edit)
    edit_area.configure(background='white')
    edit_area.insert(END, str(json.load(open('notes.json', 'r')).get(name)))
    edit_area.place(height=280, width=420, x=0, y=28)

    edit_confirm = Button(note_edit)
    edit_confirm.configure(text='Сохранить', command=set_note)
    edit_confirm.place(width=100, height=30, x=0, y=330)

    note_edit.mainloop()


def choose_note():
    note_choose = Tk()
    note_choose.title('Выберите заметку')
    note_choose.geometry('200x300')
    with open('notes.json', 'r') as f:
        notes = json.load(f)
    notes_list = Listbox(note_choose)
    for k, v in dict(notes).items():
        notes_list.insert(END, k)

    def go_to_note():
        name = notes_list.get(notes_list.curselection())
        note_choose.destroy()
        edit_note(name)

    notes_list.bind("<<ListboxSelect>>", lambda x: go_to_note())
    notes_list.pack()
    note_choose.mainloop()


def create_note():
    note_create = Tk()
    note_create.geometry('200x300')
    note_create.resizable(False, False)
    err_lbl = Label(note_create)
    err_lbl.configure(background="white")
    err_lbl.pack(anchor="center")
    with open('notes.json', 'r') as f:
        notes = json.load(f)
    new_note_name = Entry(note_create)

    def get_name():
        if str(new_note_name.get()) not in [k for k, v in json.load(open('notes.json', 'r')).items()] and \
                str(new_note_name.get()):
            notes[''.join([i for i in new_note_name.get()])] = 'text'
            with open('notes.json', 'w') as f:
                json.dump(notes, f, indent=4)
            err_lbl.pack_forget()
            err_lbl.configure(background="white", text="")
            err_lbl.pack(anchor="center")
            name = new_note_name.get()
            note_create.destroy()
            edit_note(name)
        else:
            err_lbl.pack_forget()
            err_lbl.configure(background="red", foreground="white", text="Имя заметки занято!")
            err_lbl.pack(anchor="center")

    new_note_submit = Button(note_create)
    new_note_submit.configure(text='Создать', command=get_name, background="black", foreground="white")
    new_note_name.place(height=26, width=100, x=50, y=100)
    new_note_submit.place(height=26, width=90, x=55, y=140)
    note_create.mainloop()


root = Tk()
root.title('Выберите действие')
root.geometry('200x300')
root.resizable(False, False)

new_note = Button(root)
new_note.configure(text='Новая заметка', command=create_note)
new_note.place(x=30, y=80, width=140, height=30)
existing_note = Button(root)
existing_note.configure(text='Существующая заметка', command=choose_note)
existing_note.place(x=30, y=120, width=140, height=30)

root.mainloop()
