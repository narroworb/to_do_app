from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry
import datetime
import json

def initialize():
    window = Tk()
    window.title("TO-DO APP")
    window.geometry("1400x1000")
    window.config(bg="#171C2D")
    window.resizable(width=False, height=False)
    text1 = Label(window, text="To-Do List", font=("Flame-Bold", 40), fg="#E37239", bg="#171C2D")
    text1.pack()
    text2 = Label(window, text="Добавление новой задачи:", font=("Flame-Bold", 17), fg="#E37239", bg="#171C2D")
    text2.place(x=10, y=70)

    return window

def get_from_json():
    with open('todolist.json', 'r') as file:
        non_sorted_todolist = json.load(file)
    todolist_by_completed = dict(sorted(non_sorted_todolist.items(), key=lambda item: item[1]['completed'], reverse=True))
    todolist = dict(sorted(todolist_by_completed.items(), key=lambda item: item[1]['due_date']))
    return todolist

def write_to_json(todolist):
    with open('todolist.json', 'w') as file:
        json.dump(todolist, file)

def delete_todo(item):
    global window, buttons_by_label
    todolist = get_from_json()
    del todolist[item]
    write_to_json(todolist)
    buttons_by_label[item][0].destroy()
    buttons_by_label[item][1].destroy()
    buttons_by_label[item][2].destroy()
    del buttons_by_label[item]
    update_label()

def add_todo():
    global new_todo, window, calendar
    todolist = get_from_json()
    new_item = new_todo.get()
    due_date = str(calendar.get_date())[-2:] + '.' + str(calendar.get_date())[-5:-3] + '.' + str(calendar.get_date())[:4]
    if len(new_item.split()) == 0:
        messagebox.showerror("Error", "Задача не может быть пустой")
        return
    if new_item in todolist:
        if due_date == todolist[new_item]['due_date']:
            messagebox.showerror("Error", "Такая задача уже есть")
            return
        else:
            new_item = new_item + " на " + due_date
    if new_item.isdigit():
        messagebox.showerror("Error", "Задача не может содержать только цифры")
        return
    todolist[new_item] = {"completed": False, "due_date": str(due_date)}
    new_todo.delete(0, END)
    write_to_json(todolist)
    update_label()

def select_label(item, completed, due_date):
    todolist = get_from_json()
    current_date = str(datetime.date.today())[-2:] + '.' + str(datetime.date.today())[-5:-3] + '.' + str(datetime.date.today())[:4]
    if due_date < current_date and not completed:
        label_text = f"{item}: {'Просрочена'} | Была до: {due_date}"
        label = Label(frame, width=76, text=label_text, justify=LEFT, font=("Flame-Bold", 20),
                      fg="#BB2233", bg="#171C2D", relief=GROOVE, bd=5)
    elif due_date == current_date and not completed:
        label_text = f"{item}: {'Выполнена' if completed else 'Не выполнена'} | До: {due_date}"
        label = Label(frame, width=76, text=label_text, justify=LEFT, font=("Flame-Bold", 20),
                      fg="#E37239", bg="#171C2D", relief=GROOVE, bd=5)
    else:
        label_text = f"{item}: {'Выполнена' if completed else 'Не выполнена'} | До: {due_date}"
        label = Label(frame, width=76, text=label_text, justify=LEFT, font=("Flame-Bold", 20),
                      fg=f"{'green' if todolist[item]['completed'] else '#FAE3CF'}", bg="#171C2D", relief=GROOVE, bd=5)
    return label

def complete_todo(item):
    global window, buttons_by_label
    todolist = get_from_json()
    todolist[item]['completed'] = not todolist[item]['completed']
    write_to_json(todolist)
    buttons_by_label[item][2].config(text=f"{'❌' if todolist[item]['completed'] else '✔'}")
    update_label()

def update_label():
    global buttons_by_label, frame, canvas
    todolist = get_from_json()

    for widget in frame.winfo_children():
        widget.destroy()

    y0 = 0
    for item, data in todolist.items():
        completed = data['completed']
        due_date = data['due_date']
        label = select_label(item, completed, due_date)
        label.grid(row=y0, column=0, pady=5, padx=5)

        delete_button = Button(frame, text='🗑', font=("Arial", 17), width=3, fg="#000000", bg="#FFFFFF",
                               command=lambda item=item: delete_todo(item))
        delete_button.grid(row=y0, column=2, pady=5, padx=5)

        completed_button = Button(frame, text=f"{'❌' if completed else '✔'}", font=("Arial", 17), width=3,
                                  fg="#E37239", bg="#FFFFFF", command=lambda item=item: complete_todo(item))
        completed_button.grid(row=y0, column=1, pady=5, padx=5)

        buttons_by_label[item] = (label, delete_button, completed_button)
        y0 += 1

    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


if __name__ == '__main__':
    buttons_by_label = {}
    window = initialize()
    canvas = Canvas(window, bg="#171C2D", highlightthickness=0, bd=0)
    canvas.place(x=0, y=150, width=1400, height=850)

    scrollbar = Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollbar.place(x=1378, y=150, height=850)

    canvas.config(yscrollcommand=scrollbar.set)

    frame = Frame(canvas, bg="#171C2D")
    canvas.create_window((0, 0), window=frame, anchor="nw")

    new_todo = Entry(window, width=60, font=("Flame-Bold", 22), fg="#E37239", bg="#FFFFFF")
    new_todo.place(x=10, y=100)

    calendar = DateEntry(window, width=9, font=("Flame-Bold", 21), background="darkblue", foreground="white", borderwidth=0, year=2024, firstweekday='monday', date_pattern='dd.mm.yyyy')
    calendar.place(x=1104, y=100)

    submit = Button(window, text="Submit", font=("Flame-Bold", 14), fg="#000000", bg="#FFFFFF", command=add_todo)
    submit.place(x=1300, y=100)

    update_label()
    window.mainloop()
