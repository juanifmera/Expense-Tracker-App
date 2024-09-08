import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

gastos_acumulados = {
    "id":[],
    "fecha":[],
    "titulo":[],
    "dinero":[],
    "categoria":[]
}

def menu():
    print("----" * 10)
    print("INDIQUE QUE ACCION QUIERE REALIZAR")
    print("----" * 10)
    print("(A), para Agregar un nuevo gasto")
    print("(M), para Modificar algun gasto")
    print("(E), para Eliminar algun gasto")
    print("(L), para Listar todos los gastos")
    print("(T), para ver el total de tus gastos acumulados")
    print("(G) para ver algunos graficos relacionados con sus Gastos")
    print("Cualquier otra tecla para finalizar")
    print("----" * 10)

def agregar_gasto():
    id = int(input("Agregue un identificador numerico --> "))
    fecha = input("Indique la fecha en la que realizo el gasto con el siguiente formato: DD/MM/YYYY --> ").lower()
    titulo = input("Porfavor, coloque un titulo para identificar el gasto --> ").lower()
    cantidad_dinero = float(input("Porfavor coloque la cantidad de dinero que haya gastado --> "))
    categoria = input("Porfavor introduzca alguna categoria para agrupar el gasto --> ").lower()
    
    gastos_acumulados["id"].append(id)
    gastos_acumulados["fecha"].append(fecha)
    gastos_acumulados["titulo"].append(titulo)
    gastos_acumulados["dinero"].append(cantidad_dinero)
    gastos_acumulados["categoria"].append(categoria)

    print(f"!!!Gasto Agregado!!!")

def eliminar_gasto():
    id_producto_a_eliminar = int(input("Porfavor, coloque el identificador del gasto que quiere eliminar --> "))

    if id_producto_a_eliminar in gastos_acumulados["id"]:
        indice_gasto = gastos_acumulados["id"].index(id_producto_a_eliminar)

        gastos_acumulados["id"].pop(indice_gasto)
        gastos_acumulados["fecha"].pop(indice_gasto)
        gastos_acumulados["titulo"].pop(indice_gasto)
        gastos_acumulados["dinero"].pop(indice_gasto)
        gastos_acumulados["categoria"].pop(indice_gasto)

        print("!!!Gasto Eliminado!!!")

    else:
        print("No se encotro ningun gasto registrado con ese ID")

def modificar_gasto():
    id_gasto_a_modificar = int(input("Porfavor, coloque el identificador del gasto que quiere modificar --> "))

    if id_gasto_a_modificar in gastos_acumulados["id"]:
        indice_gasto = gastos_acumulados["id"].index(id_gasto_a_modificar)

        nuevo_id = int(input("Ingrese su Nuevo ID --> "))
        nueva_fecha = input("Ingrese su nueva fecha --> ").lower()
        nuevo_titulo = input("Ingrese su Nuevo Titulo --> ").lower()
        nueva_cantidad = float(input("Ingrese su Nueva Cantidad --> "))
        nueva_categoria = input("Ingrese su nueva Categoria --> ").lower()

        gastos_acumulados["id"][indice_gasto] = nuevo_id
        gastos_acumulados["fecha"][indice_gasto] = nueva_fecha
        gastos_acumulados["titulo"][indice_gasto] = nuevo_titulo
        gastos_acumulados["dinero"][indice_gasto] = nueva_cantidad
        gastos_acumulados["categoria"][indice_gasto] = nueva_categoria

        print("!!!Su cambio se realizo Correctamente!!!") 

    else:
        print("No se encotro ningun gasto registrado con ese ID")

def listar_gastos():
    for indice, i in enumerate(range(len(gastos_acumulados["id"]))):
        print("---" * 10)
        print(indice + 1)
        print("---" * 10)
        print(f"ID: {gastos_acumulados["id"][i]}")
        print(f"FECHA: {gastos_acumulados["fecha"][i]}")
        print(f"TITULO: {gastos_acumulados["titulo"][i]}")
        print(f"DINERO: {gastos_acumulados["dinero"][i]}")
        print(f"CATEGORIA: {gastos_acumulados["categoria"][i]}")

def gastos_totales():
    total = sum(gastos_acumulados["dinero"])
    print(f"El total acumulo de sus gastos es {total}$ pesos")

def graficos():
    if len(gastos_acumulados["id"]) >= 1:
        df = pd.DataFrame(gastos_acumulados, index=gastos_acumulados["id"])
        df.reset_index(drop=True)
        df['fecha'] = pd.to_datetime(df['fecha'], format='%d/%m/%Y')

        sns.set_style("darkgrid")
        plt.figure(figsize=(10,6))
        sns.histplot(df, x="categoria", weights="dinero", bins=10)
        plt.title("Distribución de Gastos por Categoría")
        plt.xlabel("Categorías")
        plt.ylabel("Dinero $$$")
        plt.xticks(rotation=45)
        plt.show()

        df["mes"] = df["fecha"].dt.month_name()
        plt.figure(figsize=(10,6))
        sns.barplot(data=df, x="mes", y="dinero", estimator=sum, palette="viridis")
        plt.title("Gastos totales por Mes")
    
        plt.xlabel("Mes")
        plt.ylabel("Monto Gastado")
        plt.xticks(rotation=45)
        plt.show()

        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df, x="categoria", y="dinero", palette="Set2")
        plt.title("Distribución de Gastos por Categoría")
        plt.ylabel("Monto gastado")
        plt.xlabel("Categoría")
        plt.xticks(rotation=45)
        plt.show()

        plt.figure(figsize=(10, 6))
        sns.lineplot(data=df, x="fecha", y="dinero", marker="o", ci=None)
        plt.title("Evolución de Gastos a lo Largo del Tiempo")
        plt.ylabel("Monto gastado")
        plt.xlabel("Fecha")
        plt.xticks(rotation=45)
        plt.show()
    else:
        print("No hay suficientes datos para generar graficos")

while True:
    menu()

    eleccion = input("INDIQUE AQUI SU ENTRADA --> ").lower()

    if eleccion == "a":
        agregar_gasto()

    elif eleccion == "m":
        modificar_gasto()

    elif eleccion == "e":
        eliminar_gasto()

    elif eleccion == "l":
        listar_gastos()

    elif eleccion == "t":
        gastos_totales()
    
    elif eleccion == "g":
        graficos()

    else:
        print("Saliendo del programa ....")
        break