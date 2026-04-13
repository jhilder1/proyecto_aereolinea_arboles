import json
import os

# NOTE: Tkinter has been removed to avoid interfering with the web backend API.

def load_json(file_path):
    """
    Loads a JSON file from the specified path.
    
    Args:
        file_path (str): Path to the JSON file.
    
    Returns:
        dict or list: Data loaded from the JSON file.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If there is an error decoding the JSON.
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist.")
    
    # Open and load the JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding the JSON file: {e}")

def validate_flight(flight):
    """
    Validates that a flight object has all required fields
    and that their data types are correct.
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

    # Validate basic types (Simplified to not block useful mixed types from the Professor)
    if flight.get("codigo") is None:
        raise ValueError("Field 'codigo' cannot be null")

    if not isinstance(flight["origen"], str):
        raise ValueError("Field 'origen' must be a string")

    if not isinstance(flight["destino"], str):
        raise ValueError("Field 'destino' must be a string")

    if not isinstance(flight["horaSalida"], str):
        raise ValueError("Field 'horaSalida' must be a string")

    if not isinstance(flight["precioBase"], (int, float)):
        raise ValueError("Field 'precioBase' must be numeric")

    if not isinstance(flight["pasajeros"], int):
        raise ValueError("Field 'pasajeros' must be an integer")

    if not isinstance(flight["prioridad"], int):
        raise ValueError("Field 'prioridad' must be an integer")

    if not isinstance(flight["promocion"], bool):
        raise ValueError("Field 'promocion' must be a boolean")

    if not isinstance(flight["alerta"], bool):
        raise ValueError("Field 'alerta' must be a boolean")


def load_insert_data(data):
    """
    Validates an in-memory JSON dictionary in insertion mode.
    The file must have an object with "tipo": "INSERCION", "ordenamiento", and "vuelos" as a list.
    """
    if not isinstance(data, dict):
        raise ValueError("The JSON file must contain an object with 'vuelos'.")
    
    if "tipo" not in data or data["tipo"] != "INSERCION":
        raise ValueError("The file must have 'tipo': 'INSERCION'.")
    if "ordenamiento" not in data:
        raise ValueError("Missing 'ordenamiento' field.")
    if "vuelos" not in data or not isinstance(data["vuelos"], list):
        raise ValueError("Missing 'vuelos' field or it is not a list.")
    
    for flight in data["vuelos"]:
        validate_flight(flight)
    
    return data["vuelos"]

def load_topology_data(data):
    """
    Validates and loads a dictionary in topology mode.
    """
    if not isinstance(data, dict):
        raise ValueError("The topology JSON file must contain an object representing the root.")
    return data

def load_insert_json(file_path):
    """
    Loads and validates a JSON file from disk in insertion mode.
    """
    data = load_json(file_path)
    return load_insert_data(data)

def load_topology_json(file_path):
    """
    Loads a JSON file from disk in topology mode.
    """
    data = load_json(file_path)
    return load_topology_data(data)




        