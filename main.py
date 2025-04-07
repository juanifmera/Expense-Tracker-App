from tkinter import Tk
from controller import ExpenseController, ChartUpdater, MessageLogger

# Punto de entrada de la aplicación
if __name__ == "__main__":
    # Crear ventana principal de la app
    root = Tk()

    # Inicializar el controlador, que gestiona modelo y vista
    controller = ExpenseController(root)

    # Crear observadores:
    # - Uno para actualizar el gráfico automáticamente
    # - Otro para mostrar logs en consola
    chart_updater = ChartUpdater(controller)
    message_logger = MessageLogger()

    # Registrar los observadores en el controlador
    controller.add_observer(chart_updater)
    controller.add_observer(message_logger)

    # Iniciar el loop de la interfaz gráfica (Tkinter)
    root.mainloop()
