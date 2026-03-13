import json
import os

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
    Valida que un objeto de vuelo tenga todos los campos requeridos.
    
    Args:
        flight (dict): Objeto que representa un vuelo.
    
    Raises:
        Exception: Si falta algún campo requerido.
    """
    # Campos requeridos para un vuelo
    required_fields = ["codigo", "origen", "destino", "horaSalida", "precioBase", "pasajeros", "prioridad", "promocion", "alerta"]
    
    # Verificar cada campo requerido
    for field in required_fields:
        if field not in flight:
            raise Exception(f"Falta el campo '{field}' en el vuelo")

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
        