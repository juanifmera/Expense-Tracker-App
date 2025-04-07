# 💸 Expense Tracker App

Una aplicación de escritorio desarrollada en Python con interfaz gráfica (Tkinter) que permite **gestionar tus gastos personales**, organizarlos por categorías, y visualizar los totales con gráficos.

Este proyecto es ideal para quienes desean tener un control simple, local y visual de sus finanzas 💰📊

---

## 🧠 ¿Qué hace esta app?

- Permite agregar, editar y eliminar gastos diarios.
- Clasifica los gastos por **categorías personalizables**.
- Muestra los datos en una tabla ordenada.
- Calcula **totales por categoría**.
- Genera un gráfico de barras dinámico con **matplotlib**.
- Está construida bajo el patrón **MVC** + **Observer** para una arquitectura limpia y escalable.
- Utiliza **Peewee ORM** para interactuar con una base de datos SQLite.

---

## 🛠️ Tecnologías utilizadas

- **Python 3.10+**
- **Tkinter** – Interfaz gráfica
- **Peewee** – ORM liviano para base de datos
- **SQLite** – Almacenamiento local de datos
- **Matplotlib** – Visualización de gastos en gráfico
- **Pandas** – Manipulación de datos para visualización
- **Tkcalendar** – Selector de fecha visual
- **Decoradores** – Para log de acciones como creación, edición y eliminación

---

## 📂 Estructura del Proyecto

```plaintext
Expense-Tracker-App/
│
├── controller.py      # Lógica y conexión entre modelo y vista
├── model.py           # Modelo de datos con Peewee ORM
├── view.py            # Interfaz gráfica con Tkinter
├── main.py            # Archivo principal para ejecutar la app
├── decorators.py      # Decoradores para registrar acciones
├── requirements.txt   # Dependencias del proyecto
└── README.md          # Este archivo :)

