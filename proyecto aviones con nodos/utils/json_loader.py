import json
import os
from tkinter import Tk, filedialog

def select_json_file():
    """
    Abre una ventana para que el usuario seleccione un archivo JSON.

    Returns:
        str: Ruta del archivo seleccionado o None si el usuario cancela.
    """

    root = Tk()
    root.withdraw()  # Oculta la ventana principal de tkinter

    file_path = filedialog.askopenfilename(
        title="Seleccionar archivo JSON",
        filetypes=[("Archivos JSON", "*.json")]
    )

    return file_path

def load_json(file_path):
    """
    Carga un archivo JSON desde la ruta especificada.
    
    Args:
        file_path (str): Ruta al archivo JSON.
    
    Returns:
        dict or list: Datos cargados del archivo JSON.
    
    Raises:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si hay un error al decodificar el JSON.
    """
    # Verificar si el archivo existe
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo {file_path} no existe.")
    
    # Abrir y cargar el archivo JSON
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Error al decodificar el archivo JSON: {e}")

def validate_flight(flight):
    """
    Valida que un objeto de vuelo tenga todos los campos requeridos
    y que los tipos de datos sean correctos.
    """

    required_fields = [
        "codigo",
        "origen",
        "destino",
        "horaSalida",
        "precioBase",
        "pasajeros",
        "prioridad",
        "promocion",
        "alerta"
    ]

    for field in required_fields:
        if field not in flight:
            raise ValueError(f"Falta el campo '{field}' en el vuelo")

    # Validar tipos básicos
    if not isinstance(flight["codigo"], str):
        raise ValueError("El campo 'codigo' debe ser un string")

    if not isinstance(flight["origen"], str):
        raise ValueError("El campo 'origen' debe ser un string")

    if not isinstance(flight["destino"], str):
        raise ValueError("El campo 'destino' debe ser un string")

    if not isinstance(flight["horaSalida"], str):
        raise ValueError("El campo 'horaSalida' debe ser un string")

    if not isinstance(flight["precioBase"], (int, float)):
        raise ValueError("El campo 'precioBase' debe ser numérico")

    if not isinstance(flight["pasajeros"], int):
        raise ValueError("El campo 'pasajeros' debe ser un entero")

    if not isinstance(flight["prioridad"], int):
        raise ValueError("El campo 'prioridad' debe ser un entero")

    if not isinstance(flight["promocion"], bool):
        raise ValueError("El campo 'promocion' debe ser booleano")

    if not isinstance(flight["alerta"], bool):
        raise ValueError("El campo 'alerta' debe ser booleano")


def load_insert_json(file_path):
    """
    Carga y valida un archivo JSON en modo inserción.
    El archivo debe tener un objeto con "tipo": "INSERCION", "ordenamiento", y "vuelos" como lista.
    
    Args:
        file_path (str): Ruta al archivo JSON.
    
    Returns:
        dict: Datos validados con la lista de vuelos.
    
    Raises:
        ValueError: Si el formato no es correcto o faltan campos.
    """
    # Cargar los datos JSON
    data = load_json(file_path)
    
    # Verificar que sea un diccionario
    if not isinstance(data, dict):
        raise ValueError("El archivo JSON debe contener un objeto con 'vuelos'.")
    
    # Verificar campos principales
    if "tipo" not in data or data["tipo"] != "INSERCION":
        raise ValueError("El archivo debe tener 'tipo': 'INSERCION'.")
    if "ordenamiento" not in data:
        raise ValueError("Falta el campo 'ordenamiento'.")
    if "vuelos" not in data or not isinstance(data["vuelos"], list):
        raise ValueError("Falta el campo 'vuelos' o no es una lista.")
    
    # Validar cada vuelo en la lista
    for flight in data["vuelos"]:
        validate_flight(flight)
    
    return data

def load_topology_json(file_path):
    """
    Carga un archivo JSON en modo topología, que representa la estructura de un árbol AVL.
    
    Args:
        file_path (str): Ruta al archivo JSON.
    
    Returns:
        dict: Estructura del árbol cargada.
    
    Raises:
        ValueError: Si el formato no es correcto.
    """
    # Cargar los datos JSON
    data = load_json(file_path)
    
    # Verificar que sea un diccionario (raíz del árbol)
    if not isinstance(data, dict):
        raise ValueError("El archivo JSON de topología debe contener un objeto que representa la raíz del árbol.")
    
    # Aquí se podría agregar validación adicional para la estructura del árbol,
    # pero por simplicidad, asumimos que el JSON está bien formado.

    return data




        