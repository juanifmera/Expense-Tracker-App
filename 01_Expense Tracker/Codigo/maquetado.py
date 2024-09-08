import os
import sqlite3
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.messagebox import *
import re

# Genero la App
window = Tk()
window.title("Expense Tracker")
window.geometry("600x600")
window.maxsize(width=900, height=600)
window.minsize(width=900, height=600)

# Obtener la ubicación del archivo ejecutable
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "expense_tracker.db")

# Conecto la base de datos en la ubicación del archivo ejecutable
db = sqlite3.connect(db_path)

# Crear la tabla principal si no existe
cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    title TEXT,
                    amount REAL,
                    category TEXT)""")
db.commit()

# Crear la tabla de categorias si no existe
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY AUTOINCREMENT, category_name TEXT NOT NULL)")
db.commit()

# Configurar las filas y columnas en la ventana principal
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=0)
window.grid_columnconfigure(1, weight=1)

# Primer Frame --> Inputs
input_frame = Frame(window, width=200, height=700)
input_frame.grid_propagate(False)
input_frame.grid(row=0, column=0, sticky=N+S)
input_frame.grid_columnconfigure(0, weight=1)

# Segundo Frame --> Grafico 1
graph_frame = Frame(window, width=350, height=290)
graph_frame.grid_propagate(False)
graph_frame.grid(row=0, column=1, sticky=NW)
graph_frame.grid_columnconfigure(0, weight=1)
graph_frame.grid_rowconfigure(0, weight=1)

# Tercer Frame --> Grafico 2
graph_frame1 = Frame(window, width=350, height=290)
graph_frame1.grid_propagate(False)
graph_frame1.grid(row=0, column=1, sticky=NE)
graph_frame1.grid_columnconfigure(0, weight=1)
graph_frame1.grid_rowconfigure(0, weight=1)

# Cuarto Frame --> Tabla
table_frame = Frame(window, width=700, height=310)
table_frame.grid_propagate(False)
table_frame.grid(row=0, column=1, sticky=S)
table_frame.grid_columnconfigure(0, weight=1)
table_frame.grid_rowconfigure(0, weight=1)

# Genero Variables
date_var = StringVar()
title_var = StringVar()
amount_var = DoubleVar()
category_var = StringVar()
add_category_popup_var = StringVar()

# Genero Funciones
def add_expense():
    title = title_var.get()
    
    if not title:
        message.config(text="Error: El campo 'Title' no puede estar vacío.", fg="red")
        return
    
    regex = r'^[A-Za-z\s]+$'
    
    if not re.match(regex, title):
        message.config(text="Error: El campo 'Title' solo debe contener letras.", fg="red")
        return
    
    data = (date_var.get(), title, amount_var.get(), category_var.get())
    cursor = db.cursor()
    sql = "INSERT INTO expenses(date, title, amount, category) VALUES(?, ?, ?, ?)"
    cursor.execute(sql, data)
    db.commit()
    
    get_expenses()
    date_var.set(""), title_var.set(""), amount_var.set(""), category_var.set("")
    update_charts()

    message.config(text="Gasto agregado exitosamente.", fg="green")

def delete_expense():
    selected_item = tree.selection()
    if selected_item:
        item_id = tree.item(selected_item)["values"][0]  
        cursor = db.cursor()
        sql = "DELETE FROM expenses WHERE id = ?"
        cursor.execute(sql, (item_id,))
        db.commit()
        get_expenses()
        update_charts()

def edit_expense():
    selected_item = tree.selection()
    if not selected_item:
        return
    
    item_id = tree.item(selected_item)["values"][0]

    cursor = db.cursor()
    sql = "SELECT date, title, amount, category FROM expenses WHERE id = ?"
    cursor.execute(sql, (item_id,))
    current_values = cursor.fetchone()

    if not current_values:
        return

    edit_window = Toplevel(window)
    edit_window.title("Edit Expense")
    edit_window.geometry("400x360")
    edit_window.grid_columnconfigure(0, weight=1)
    edit_window.grid_columnconfigure(1, weight=1)

    current_title = Label(edit_window, text="Current Values", font=("Arial", 12, "bold"))
    current_title.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

    date_label = Label(edit_window, text="Date:")
    date_label.grid(row=1, column=0, sticky=W, padx=5, pady=5)
    date_value = Label(edit_window, text=current_values[0])
    date_value.grid(row=1, column=1, sticky=W, padx=5, pady=5)

    title_label = Label(edit_window, text="Title:")
    title_label.grid(row=2, column=0, sticky=W, padx=5, pady=5)
    title_value = Label(edit_window, text=current_values[1])
    title_value.grid(row=2, column=1, sticky=W, padx=5, pady=5)

    amount_label = Label(edit_window, text="Amount:")
    amount_label.grid(row=3, column=0, sticky=W, padx=5, pady=5)
    amount_value = Label(edit_window, text=current_values[2])
    amount_value.grid(row=3, column=1, sticky=W, padx=5, pady=5)

    category_label = Label(edit_window, text="Category:")
    category_label.grid(row=4, column=0, sticky=W, padx=5, pady=5)
    category_value = Label(edit_window, text=current_values[3])
    category_value.grid(row=4, column=1, sticky=W, padx=5, pady=5)

    new_title = Label(edit_window, text="New Values", font=("Arial", 12, "bold"))
    new_title.grid(row=5, column=0, padx=5, pady=5, columnspan=2)

    new_date_var = StringVar(value=current_values[0])
    new_title_var = StringVar(value=current_values[1])
    new_amount_var = DoubleVar(value=current_values[2])
    new_category_var = StringVar(value=current_values[3])

    new_date_label = Label(edit_window, text="New Date:")
    new_date_label.grid(row=6, column=0, sticky=W, padx=5, pady=5)
    new_date_entry = DateEntry(edit_window, textvariable=new_date_var, width=18, background="darkblue", foreground="white", borderwidth=2)
    new_date_entry.grid(row=6, column=1, sticky=W+E, padx=5, pady=5)

    new_title_label = Label(edit_window, text="New Title:")
    new_title_label.grid(row=7, column=0, sticky=W, padx=5, pady=5)
    new_title_entry = Entry(edit_window, textvariable=new_title_var)
    new_title_entry.grid(row=7, column=1, sticky=W+E, padx=5, pady=5)

    new_amount_label = Label(edit_window, text="New Amount:")
    new_amount_label.grid(row=8, column=0, sticky=W, padx=5, pady=5)
    new_amount_entry = Entry(edit_window, textvariable=new_amount_var)
    new_amount_entry.grid(row=8, column=1, sticky=W+E, padx=5, pady=5)

    new_category_label = Label(edit_window, text="New Category:")
    new_category_label.grid(row=9, column=0, sticky=W, padx=5, pady=5)
    new_category_entry = ttk.Combobox(edit_window, textvariable=new_category_var, values=category_combobox["values"])
    new_category_entry.grid(row=9, column=1, sticky=W+E, padx=5, pady=5)

    def confirm_edit():
        updated_data = (
            new_date_var.get(),
            new_title_var.get(),
            new_amount_var.get(),
            new_category_var.get(),
            item_id
        )
        sql = "UPDATE expenses SET date = ?, title = ?, amount = ?, category = ? WHERE id = ?"
        cursor.execute(
            sql,
            updated_data
        )
        db.commit()
        get_expenses()
        edit_window.destroy()
        update_charts()

    confirm_button = Button(edit_window, text="Confirm Changes", command=confirm_edit)
    confirm_button.grid(row=10, column=0, columnspan=2, padx=5, pady=10, sticky=W+E)

def get_expenses():
    records = tree.get_children()
    for element in records:
        tree.delete(element)

    cursor = db.cursor()
    cursor.execute("SELECT * FROM expenses ORDER BY id DESC")
    db_rows = cursor.fetchall()

    for row in db_rows:
        tree.insert("", "end", values=row)

def load_categories():
    cursor = db.cursor()
    sql = "SELECT category_name FROM categories"
    cursor.execute(sql)
    categories = cursor.fetchall()
    
    category_list = [category[0] for category in categories]
    
    category_combobox["values"] = category_list
    
    if category_list:
        category_combobox.set(category_list[0])

def add_category_window():

    def suscribe_category():
        new_category = add_category_popup_var.get()
        cursor = db.cursor()
        sql = "INSERT INTO categories (category_name) VALUES (?)"
        cursor.execute(sql, (new_category,))
        db.commit()
        load_categories()
        add_category_popup.destroy()

    add_category_popup = Toplevel(window)
    add_category_popup.title("Add Category")
    add_category_popup.geometry("220x80")
    add_category_popup.minsize(width=200, height=80)
    add_category_popup.maxsize(width=200, height=80)

    add_category_popup.grid_columnconfigure(0, weight=1)

    add_category_popup_label = Label(add_category_popup, text="Please subscribe new Category", font=("Arial", 10))
    add_category_popup_label.grid(row=0, column=0, sticky=E+W, padx=2, pady=2)
    
    add_category_popup_entry = Entry(add_category_popup, textvariable=add_category_popup_var)
    add_category_popup_entry.grid(row=1, column=0, sticky=EW, padx=2, pady=2)
    
    add_category_popup_button = Button(add_category_popup, text="Add new category", command=suscribe_category)
    add_category_popup_button.grid(row=2, column=0, sticky=EW, padx=2, pady=2)

def delete_category_window():

    def insert_categories_values():
        categories = delete_category_popup_tree.get_children()
        for category in categories:
            delete_category_popup_tree.delete(category)

        db.cursor()
        sql = "SELECT * FROM categories ORDER BY id DESC"
        cursor.execute(sql)
        category_rows = cursor.fetchall()

        for row in category_rows:
            delete_category_popup_tree.insert("", "end", values=row)

    def delete_category_value():
        delete_item = delete_category_popup_tree.selection()
        if delete_item:
            delete_category_id = delete_category_popup_tree.item(delete_item)["values"][0]
            db.cursor()
            sql = "DELETE FROM categories WHERE id = ?"
            cursor.execute(sql, (delete_category_id,))
            db.commit()
            insert_categories_values()
            load_categories()

    delete_category_popup = Toplevel(window)
    delete_category_popup.title("Delete Category")
    delete_category_popup.geometry("300x290")
    delete_category_popup.minsize(width=300, height=290)
    delete_category_popup.maxsize(width=300, height=290)

    delete_category_popup.grid_columnconfigure(0, weight=1)

    delete_category_popup_label = Label(delete_category_popup, text="Please delete any Category", font=("Arial", 10))
    delete_category_popup_label.grid(row=0, column=0, sticky=E+W, padx=2, pady=2)
    
    delete_category_popup_tree = ttk.Treeview(delete_category_popup, columns=("ID", "Category"), show="headings")
    delete_category_popup_tree.grid(row=1, column=0, sticky=EW, padx=2, pady=2)
    
    delete_category_popup_button = Button(delete_category_popup, text="Delete Category", command= delete_category_value)
    delete_category_popup_button.grid(row=2, column=0, sticky=EW, padx=2, pady=2)

    delete_category_popup_tree.heading("ID", text="ID")
    delete_category_popup_tree.heading("Category", text="Category")
    delete_category_popup_tree.column("ID", anchor=CENTER, width=50)
    delete_category_popup_tree.column("Category", anchor=CENTER, width=250)
    
    insert_categories_values()

def update_charts():
    for widget in graph_frame.winfo_children():
        widget.destroy()
    for widget in graph_frame1.winfo_children():
        widget.destroy()

    sql = pd.read_sql_query("SELECT * FROM expenses", db)
    df_expenses = pd.DataFrame(sql, columns=("id", "date", "title", "amount", "category"))
    df_expenses.set_index("id", inplace=True)

    fig1, ax1 = plt.subplots(figsize=(4.5, 4))
    bars = ax1.bar(df_expenses["category"], df_expenses["amount"])
    ax1.set_title("Amount Spent by Category", fontsize=8, weight="bold")
    ax1.tick_params(axis="x", labelsize=6, rotation=15)
    ax1.tick_params(axis="y", labelsize=6)
    fig1.tight_layout()

    barchart = FigureCanvasTkAgg(fig1, graph_frame)
    barchart.draw()
    barchart.get_tk_widget().grid(row=0, column=0, sticky=NSEW)

    category_totals = df_expenses.groupby("category")["amount"].sum()
    category_percentages = category_totals / category_totals.sum() * 100

    fig2, ax2 = plt.subplots(figsize=(4.5, 4))
    colors = sns.color_palette("viridis", len(category_totals))
    wedges, texts, autotexts = ax2.pie(category_percentages, labels=category_totals.index, autopct="%1.1f%%", colors=colors, startangle=140, wedgeprops=dict(width=0.4))

    for text in texts:
        text.set_fontsize(6)
    for autotext in autotexts:
        autotext.set_fontsize(6)

    centre_circle = plt.Circle((0, 0), 0.70, color="white", fc="white", linewidth=1.25)
    ax2.add_artist(centre_circle)

    ax2.set_title("Distribution of Expenses by Category", fontsize=8, weight="bold")
    fig2.tight_layout()

    piechart = FigureCanvasTkAgg(fig2, graph_frame1)
    piechart.draw()
    piechart.get_tk_widget().grid(row=0, column=0, sticky=NSEW)

# Espacio en blanco antes de los las etiquetas principales dentro del Input Frame
empty_label = Label(input_frame, text="")
empty_label.grid(row=0, column=0, pady=40)

# Agregar etiquetas al Imput frame
date_label = Label(input_frame, text="Date", font=("Arial", 12, "bold"))
date_label.grid(row=1, column=0, sticky=W, padx=5, pady=5, columnspan=2)

title_label = Label(input_frame, text="Title", font=("Arial", 12, "bold"))
title_label.grid(row=3, column=0, sticky=W, padx=5, pady=5, columnspan=2)

amount_label = Label(input_frame, text="Amount", font=("Arial", 12, "bold"))
amount_label.grid(row=5, column=0, sticky=W, padx=5, pady=5,columnspan=2)

category_label = Label(input_frame, text="Category", font=("Arial", 12, "bold"))
category_label.grid(row=7, column=0, sticky=W, padx=5, pady=5, columnspan=2)

# Agregar campos de entrada al Input Frame
date_entry = DateEntry(input_frame, width=18, background="darkblue", foreground="white", borderwidth=2, font=("Arial", 10), textvariable= date_var)
date_entry.grid(row=2, column=0, sticky=W+E, padx=5, pady=5,columnspan=2)

title_entry = Entry(input_frame, font=("Arial", 10), textvariable= title_var)
title_entry.grid(row=4, column=0, sticky=W+E, padx=5, pady=5, columnspan=2)

amount_entry = Entry(input_frame, font=("Arial", 10), textvariable= amount_var)
amount_entry.grid(row=6, column=0, sticky=W+E, padx=5, pady=5, columnspan=2)

category_combobox = ttk.Combobox(input_frame, font=("Arial", 10), textvariable= category_var)
category_combobox.grid(row=8, column=0, sticky=W+E, padx=5, pady=5, columnspan=2)
category_combobox.set("Select a Category")

# Espacio en blanco antes de los botones
empty_label1 = Label(input_frame, text="")
empty_label1.grid(row=10, column=0, pady=15)

# Botones dentro del Input Frame
add_expense_button = Button(input_frame, text="Add Expense", height=2, font=("Arial", 12, "bold underline"), command= add_expense)
add_expense_button.grid(row=11, column=0, sticky=W+E, padx=5, pady=2, columnspan=2)

add_category_button = Button(input_frame, text="Add Category", command= add_category_window)
add_category_button.grid(row=9, column=0, sticky=W+E, padx=5)

delete_category_button = Button(input_frame, text="Delete Category", command= delete_category_window)
delete_category_button.grid(row=9, column=1, sticky=W+E, padx=5)

# Espacio en despues de los botones
empty_label2 = Label(input_frame, text="")
empty_label2.grid(row=12, column=0, pady=10)

# Crear el Message Label dentro del Input frame
message = Label(input_frame, text="", wraplength=200, anchor="center")
message.grid(row=13, column=0, sticky=E+W, columnspan=2)

# Tabla de datos
tree = ttk.Treeview(table_frame, columns=("ID", "Date", "Title", "Amount", "Category"), show="headings")
tree.grid(row=0, column=0, sticky=NSEW, columnspan=2)

# Configurar las columnas
tree.heading("ID", text="ID")
tree.heading("Date", text="Date")
tree.heading("Title", text="Title")
tree.heading("Amount", text="Amount")
tree.heading("Category", text="Category")

tree.column("ID", anchor=CENTER, width=50)
tree.column("Date", anchor=CENTER, width=100)
tree.column("Title", anchor=CENTER, width=150)
tree.column("Amount", anchor=CENTER, width=100)
tree.column("Category", anchor=CENTER, width=100)

# Botones dentro del Table Frame
edit_button = Button(table_frame, text="Edit", width=50, command= edit_expense)
edit_button.grid(row=1, column=0, sticky=S+E)

delete_button = Button(table_frame, text="Delete", width=50, command= delete_expense)
delete_button.grid(row=1, column=1, sticky=S+W)

# Genero los graficos
sql = pd.read_sql_query("SELECT * FROM expenses", db)
df_expenses = pd.DataFrame(sql, columns=("id", "date", "title", "amount", "category"))
df_expenses.set_index("id", inplace=True)

## Barchart
fig1, ax1 = plt.subplots(figsize=(4.5, 4))

bars = ax1.bar(df_expenses["category"], df_expenses["amount"])

ax1.set_title("Amount Spent by Category", fontsize=8, weight="bold")
ax1.tick_params(axis="x", labelsize=6, rotation=15)
ax1.tick_params(axis="y", labelsize=6)
fig1.tight_layout()

barchart = FigureCanvasTkAgg(fig1, graph_frame)
barchart.draw()
barchart.get_tk_widget().grid(row=0, column=0, sticky=NSEW)

## Donut Chart
category_totals = df_expenses.groupby("category")["amount"].sum()
category_percentages = category_totals / category_totals.sum() * 100

fig2, ax2 = plt.subplots(figsize=(4.5, 4))
colors = sns.color_palette("viridis", len(category_totals))
wedges, texts, autotexts = ax2.pie(category_percentages, labels= category_totals.index, colors=colors, autopct="%1.1f%%", startangle=140, wedgeprops=dict(width=0.4))

for text in texts:
    text.set_fontsize(6)
for autotext in autotexts:
    autotext.set_fontsize(6)

centre_circle = plt.Circle((0, 0), 0.70, color="white", fc="white", linewidth=1.25)
fig2.gca().add_artist(centre_circle)

ax2.set_title("Distribution of Expenses by Category", fontsize=8, weight="bold")

fig2.tight_layout()

piechart = FigureCanvasTkAgg(fig2, graph_frame1)
piechart.draw()
piechart.get_tk_widget().grid(row=0, column=0, sticky=NSEW)

# Cargo las categorias
load_categories()

# Cargo registros
get_expenses()

# Corro la App
window.mainloop()
