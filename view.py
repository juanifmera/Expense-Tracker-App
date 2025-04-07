# -------------------- IMPORTS --------------------
from tkinter import Frame, Button, Label, StringVar, DoubleVar, Entry
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# -------------------- VISTA (Tkinter) --------------------
class ExpenseView:
    """
    Clase que define la interfaz gráfica de usuario para el Expense Tracker.
    Utiliza Tkinter para la UI, y Matplotlib para la visualización de gráficos.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("600x600")
        self.root.maxsize(width=900, height=430)
        self.root.minsize(width=900, height=430)
        
        # Variables de entrada para cada campo del formulario
        self.date_var = StringVar()
        self.title_var = StringVar()
        self.amount_var = DoubleVar()
        self.category_var = StringVar()
        self.message_var = StringVar(value="")  # Para mostrar mensajes al usuario
        
        # Inicialización de componentes visuales
        self.setup_ui()
    
    def setup_ui(self):
        """
        Crea y organiza todos los widgets dentro de la ventana principal.
        """

        # Frame principal para el formulario de entrada
        input_frame = Frame(self.root, width=300, height=200)
        input_frame.grid(row=0, column=0, sticky="ew")

        # Frame para mostrar el gráfico de barras
        self.chart_frame = Frame(self.root, width=600, height=200)
        self.chart_frame.grid(row=0, column=1, sticky="we")

        # Campo fecha
        self.date_label = Label(input_frame, text="Date")
        self.date_label.grid(row=0, column=0, pady=5, sticky="e")
        self.date_entry = DateEntry(input_frame, textvariable=self.date_var)
        self.date_entry.grid(row=0, column=1, sticky="nsew")
        
        # Campo título
        self.title_label = Label(input_frame, text="Title")
        self.title_label.grid(row=1, column=0, sticky="nsew")
        self.title_entry = Entry(input_frame, textvariable=self.title_var)
        self.title_entry.grid(row=1, column=1, sticky="nsew")
        self.title_entry.insert(0, "--Enter Title--")
        
        # Campo monto
        self.amount_label = Label(input_frame, text="Amount")
        self.amount_label.grid(row=2, column=0, sticky="nsew")
        self.amount_entry = Entry(input_frame, textvariable=self.amount_var)
        self.amount_entry.grid(row=2, column=1, sticky="nsew")
        
        # Campo categoría (Combobox)
        self.category_label = Label(input_frame, text="Category")
        self.category_label.grid(row=3, column=0, sticky="nsew")
        self.category_entry = self.category_combobox = ttk.Combobox(input_frame, textvariable=self.category_var)
        self.category_entry.grid(row=3, column=1, sticky="nsew")
        self.category_entry.set("--Select Category--")

        # Espaciadores invisibles para mejor formato
        self.invisible_label1 = Label(input_frame, text="     ")
        self.invisible_label1.grid(column=2, row=0, rowspan=3)

        self.invisible_label2 = Label(input_frame, text="     ")
        self.invisible_label2.grid(column=4, row=0, rowspan=3)

        # Mensaje al usuario (errores, confirmaciones, etc.)
        self.message_label = Label(input_frame, textvariable=self.message_var, anchor="center", wraplength=150, width=20, height=10)
        self.message_label.grid(row=0, rowspan=4, column=5, sticky="nsew")
        
        # Botones principales
        self.add_button = Button(input_frame, text="Add Expense")
        self.add_button.grid(row=0, column=3, columnspan=1, sticky="nsew")
        
        self.delete_button = Button(input_frame, text="Delete Expense")
        self.delete_button.grid(row=1, column=3, columnspan=1, sticky="nsew")
        
        self.edit_button = Button(input_frame, text="Edit Expense")
        self.edit_button.grid(row=2, column=3, columnspan=1, sticky="nsew")

        self.total_button = Button(input_frame, text="Calculate totals")
        self.total_button.grid(row=3, column=3, columnspan=1, sticky="nsew")
        
        # Frame para la tabla con los gastos
        table_frame = Frame(self.root, width=900, height=400)
        table_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")

        # Tabla TreeView para mostrar gastos
        self.tree = ttk.Treeview(table_frame, columns=("ID", "Date", "Title", "Amount", "Category"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Category", text="Category")

        # Configuración de columnas
        self.tree.column("ID", anchor="center", width=50)
        self.tree.column("Date", anchor="center", width=100)
        self.tree.column("Title", anchor="center", width=150)
        self.tree.column("Amount", anchor="center", width=100)
        self.tree.column("Category", anchor="center", width=100)

        # Mostrar la tabla
        self.tree.pack(fill="both", expand=True)
    
    def display_chart(self, fig):
        """
        Muestra el gráfico de barras dentro del frame derecho.
        """
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def load_categories(self):
        """
        Carga las categorías disponibles en el combobox.
        """
        categories = self.model.get_categories()
        self.category_combobox['values'] = categories 
        if categories:
            self.category_combobox.current(0)

    def set_controller(self, controller):
        """
        Asocia los botones a los métodos del controlador.
        """
        self.add_button.config(command=controller.add_expense)
        self.delete_button.config(command=controller.delete_expense)
        self.edit_button.config(command=controller.edit_expense)
        self.total_button.config(command=controller.calculate_totals)

    def update_message(self, message, color="black"):
        """
        Actualiza el mensaje mostrado al usuario.
        """
        self.message_var.set(message)
        self.message_label.config(fg=color)

    def clear_fields(self):
        """
        Limpia los campos de entrada del formulario.
        """
        self.date_var.set(datetime.now().strftime("%m/%d/%Y"))
        self.title_var.set("")
        self.title_entry.insert(0, "--Enter Title--")
        self.amount_var.set(0.0)
        self.category_entry.set("--Select Category--")
    
    def set_edit_fields(self, date, title, amount, category):
        """
        Carga los datos de un gasto seleccionado para su edición.
        """
        self.date_var.set(date)
        self.title_var.set(title)
        self.amount_var.set(amount)
        self.category_var.set(category)
