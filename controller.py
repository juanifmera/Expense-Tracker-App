# Importación de librerías necesarias
from abc import ABC, abstractmethod
from model import ExpenseModel
from view import ExpenseView
import re
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter

# -------------------- PATRÓN OBSERVER --------------------

class Subject:
    """
    Clase base para implementar el patrón Observer.
    Permite a los observadores suscribirse y recibir notificaciones de eventos.
    """
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        """Agrega un observador a la lista."""
        self._observers.append(observer)

    def remove_observer(self, observer):
        """Elimina un observador de la lista."""
        self._observers.remove(observer)

    def notify_observers(self, data):
        """Notifica a todos los observadores sobre un evento."""
        for observer in self._observers:
            observer.update(data)

class Observer(ABC):
    """
    Interfaz para los observadores en el patrón Observer.
    Define el método update() que deben implementar las subclases.
    """
    @abstractmethod
    def update(self, data):
        pass

# -------------------- CONTROLADOR PRINCIPAL --------------------

class ExpenseController(Subject):
    """
    Controlador principal que gestiona la lógica entre el modelo y la vista.
    Extiende Subject para notificar a observadores (gráfico y logger).
    """
    def __init__(self, root):
        super().__init__()
        self.model = ExpenseModel()
        self.view = ExpenseView(root)
        self.view.set_controller(self)
        self.load_categories()
        self.load_expenses()
        self.view.update_message("")
        self.editing_expense_id = None
        self.generate_chart()

    def add_expense(self):
        """
        Agrega un nuevo gasto o actualiza uno existente.
        Valida los campos antes de guardar.
        """
        date = self.view.date_var.get()
        title = self.view.title_var.get()
        amount = self.view.amount_var.get()
        category = self.view.category_var.get()

        # Validaciones básicas
        if not title or not date or not amount or not category:
            self.view.update_message("Error: Todos los campos son obligatorios.", "red")
            return

        # Validación del campo título (solo letras y espacios)
        regex = r'^[A-Za-z\s]+$'
        if not re.match(regex, title):
            self.view.update_message("Error: El campo 'Title' solo debe contener letras.", "red")
            return

        # Si se está editando un gasto existente
        if self.editing_expense_id:
            self.model.update_expense(self.editing_expense_id, date, title, amount, category)
            self.view.update_message("Expense updated successfully.", "green")
            self.editing_expense_id = None
            self.view.add_button.config(text="Add Expense")
        else:
            # Si es un gasto nuevo
            self.model.add_expense(date, title, amount, category)
            self.view.update_message("Expense has been created successfully.", "green")

        self.load_expenses()
        self.view.clear_fields()
        self.notify_observers("expense_added")

    def delete_expense(self):
        """Elimina un gasto seleccionado desde la vista."""
        selected_item = self.view.tree.selection()
        if selected_item:
            item_id = self.view.tree.item(selected_item)['values'][0]
            self.model.delete_expense(item_id)
            self.load_expenses()
            self.view.update_message("Expense has been deleted successfully.", "green")
            self.view.clear_fields()
        else:
            self.view.update_message("Error: No expense selected for deletion.", "red")

        self.notify_observers("expense_deleted")
    
    def edit_expense(self):
        """
        Carga los datos del gasto seleccionado en los campos de entrada
        para permitir su edición.
        """
        selected_item = self.view.tree.selection()
        if selected_item:
            item_values = self.view.tree.item(selected_item)['values']
            self.editing_expense_id = item_values[0]
            date = item_values[1]
            title = item_values[2]
            amount = float(item_values[3].replace(",", ""))
            category = item_values[4]
            
            self.view.set_edit_fields(date, title, amount, category)
            self.view.add_button.config(text="Save Changes")
            self.view.update_message("Edit mode: Press 'Save Changes' to update.", "blue")
        else:
            self.view.update_message("Error: No expense selected for editing.", "red")

    def load_expenses(self):
        """Carga todos los gastos desde el modelo hacia la vista."""
        for row in self.view.tree.get_children():
            self.view.tree.delete(row)

        for expense in self.model.get_expenses():
            formatted_amount = "{:,}".format(expense.amount)
            self.view.tree.insert("", "end", values=(expense.id, expense.date, expense.title, formatted_amount, expense.category))

    def load_categories(self):
        """Carga las categorías en el combobox de la vista."""
        categories = self.model.get_categories()
        self.view.category_combobox['values'] = categories
    
    def calculate_totals(self):
        """
        Calcula el total de gastos por categoría y los muestra en la vista.
        """
        totals = self.model.calculate_totals()

        if totals:
            message = "Total by Category: \n" + "\n".join(f"{category}: ${total:,.2f}" for category, total in totals)
        else:
            message = "No hay gastos registrados"
        
        self.view.update_message(message, color="blue")

    def generate_chart(self):
        """
        Genera un gráfico de barras con los gastos por categoría.
        Solo se ejecuta si hay datos disponibles.
        """
        df_expenses = self.model.get_expenses_data()
        if not df_expenses.empty:
            category_totals, _ = self.model.get_category_totals(df_expenses)
            colors = plt.cm.Blues(np.linspace(0.3, 1, len(category_totals)))
            fig, ax = plt.subplots(figsize=(4.2, 2))
            ax.bar(category_totals.index, category_totals.values, color=colors)
            ax.set_xlabel("($)", fontsize=6)
            ax.tick_params(axis="x", labelsize=6, rotation=9)
            ax.tick_params(axis="y", labelsize=6)
            ax.get_yaxis().set_major_formatter(ScalarFormatter())
            plt.subplots_adjust(top=1, bottom=0.15)
            self.view.display_chart(fig)
        else:
            self.view.update_message("No hay datos para graficar.", "red")

# -------------------- OBSERVADORES --------------------

class ChartUpdater(Observer):
    """
    Observador que actualiza el gráfico cuando se agregan o eliminan gastos.
    """
    def __init__(self, controller):
        self.controller = controller

    def update(self, data):
        if data in ["expense_added", "expense_deleted"]:
            self.controller.generate_chart()

class MessageLogger(Observer):
    """
    Observador que imprime en consola cuando ocurre un evento relevante.
    Útil para debugging o trazabilidad.
    """
    def update(self, data):
        print(f"Evento registrado: {data}")
