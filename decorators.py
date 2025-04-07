def log_new_entry(func):
    """
    Decorador para registrar en consola cuando se ingresa un nuevo registro.
    Ideal para usar en funciones que agregan datos (crear gastos, etc.).
    """
    def wrapper(*args, **kwargs):
        # Mensaje informativo previo a la ejecución
        print("Ingreso de un nuevo registro")
        result = func(*args, **kwargs)
        return result
    return wrapper

def log_update(func):
    """
    Decorador para registrar en consola cuando se actualiza un registro.
    Útil para funciones de edición o modificación de datos.
    """
    def wrapper(*args, **kwargs):
        print("Actualización de Registro Exitosa")
        result = func(*args, **kwargs)
        return result
    return wrapper

def log_deletion(func):
    """
    Decorador para registrar en consola cuando se elimina un registro.
    Se puede aplicar sobre funciones de eliminación de datos (gastos, usuarios, etc.).
    """
    def wrapper(*args, **kwargs):
        print("Registro Eliminado con éxito")
        result = func(*args, **kwargs)
        return result
    return wrapper