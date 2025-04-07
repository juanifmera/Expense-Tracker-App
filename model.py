# -------------------- IMPORTS --------------------
import sqlite3
import os
import pandas as pd
from peewee import *
from decorators import log_new_entry, log_update, log_deletion

# -------------------- CONFIGURACIÓN DE BASE DE DATOS --------------------
# Ruta absoluta del archivo actual
script_dir = os.path.dirname(os.path.abspath(__file__))

# Ruta absoluta al archivo de base de datos SQLite
db_dir = os.path.join(script_dir, 'expense_tracker.db')

# Inicializamos la base de datos con Peewee
db = SqliteDatabase(db_dir)

# -------------------- MODELOS DE DATOS --------------------

class BaseModel(Model):
    """
    Modelo base para que todos los modelos compartan la misma base de datos.
    """
    class Meta:
        database = db

class Expense(BaseModel):
    """
    Modelo para representar un gasto individual.
    """
    date = TextField()
    title = TextField()
    amount = FloatField()
    category = TextField()

class Category(BaseModel):
    """
    Modelo para representar una categoría de gastos.
    """
    category_name = TextField(unique=True)

# -------------------- LÓGICA DEL MODELO --------------------

class ExpenseModel:
    """
    Clase que gestiona todas las operaciones relacionadas a la base de datos,
    incluyendo gastos y categorías.
    """

    def __init__(self):
        try:
            db.connect()
            db.create_tables([Expense, Category], safe=True)
            self._initialize_categories()
            print("Base de datos conectada y tablas creadas correctamente")

        except OperationalError as e:
            print(f"Error al conectar o crear tablas en la base de datos: {e}")
            raise
        
        finally:
            print("Inicialización de la base de datos completada")

    def _initialize_categories(self):
        """
        Crea un conjunto inicial de categorías si la tabla está vacía.
        """
        count = Category.select().count()
        
        if count == 0:
            categories = [
                "Food & Groceries",
                "Transport & Gas",
                "Entertainment & Leisure",
                "Utilities & Bills",
                "Health & Wellness"
            ]
            for category in categories:
                self.add_category(category)

    @log_new_entry
    def add_expense(self, date, title, amount, category):
        """
        Agrega un nuevo gasto a la base de datos.
        Decorado para registrar la acción en consola.
        """
        Expense.create(date=date, title=title, amount=amount, category=category)

    def get_expenses(self):
        """
        Devuelve todos los gastos ordenados por ID descendente.
        """
        return Expense.select().order_by(Expense.id.desc())

    @log_deletion
    def delete_expense(self, expense_id):
        """
        Elimina un gasto por su ID.
        Decorado para registrar la acción en consola.
        """
        Expense.get_by_id(expense_id).delete_instance()

    @log_update
    def update_expense(self, expense_id, date, title, amount, category):
        """
        Actualiza los datos de un gasto existente por su ID.
        Decorado para registrar la acción en consola.
        """
        expense = Expense.get_by_id(expense_id)
        expense.date = date
        expense.title = title
        expense.amount = amount
        expense.category = category
        expense.save()

    def get_categories(self):
        """
        Devuelve una lista de nombres de categorías existentes.
        """
        return [category.category_name for category in Category.select()]

    def calculate_totals(self):
        """
        Calcula el total de gastos por categoría.
        Retorna una lista de tuplas con (categoría, total).
        """
        query = (
            Expense.select(Expense.category, fn.SUM(Expense.amount).alias('total'))
            .group_by(Expense.category)
        )
        return [(expense.category, expense.total) for expense in query]
    
    def get_expenses_data(self):
        """
        Devuelve todos los gastos en un DataFrame de Pandas.
        Útil para análisis o visualización.
        """
        expenses = Expense.select()
        data = [(exp.id, exp.date, exp.title, exp.amount, exp.category) for exp in expenses]
        return pd.DataFrame(data, columns=["id", "date", "title", "amount", "category"]).set_index("id")

    def get_category_totals(self, df_expenses):
        """
        Calcula totales y porcentajes por categoría a partir de un DataFrame.
        Retorna dos series: totales y porcentajes.
        """
        category_totals = df_expenses.groupby("category")["amount"].sum()
        category_percentages = category_totals / category_totals.sum() * 100
        return category_totals, category_percentages
    
    def add_category(self, category_name):
        """
        Agrega una nueva categoría si no existe.
        """
        Category.get_or_create(category_name=category_name)

    def delete_category(self, category_id):
        """
        Elimina una categoría por ID.
        """
        Category.get_by_id(category_id).delete_instance()

    def close_connection(self):
        """
        Cierra la conexión con la base de datos.
        """
        db.close()
