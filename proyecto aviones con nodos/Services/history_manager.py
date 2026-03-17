import copy
import json
import os
from datetime import datetime

class HistoryManager:
    """
    Gestiona el historial del árbol para permitir:
    - Hacer Ctrl+Z (Undo) en las operaciones.
    - Guardar versiones con nombres específicos en el sistema de archivos.
    - Cargar versiones específicas.
    """
    
    def __init__(self, max_undo_steps=20):
        self.undo_stack = []
        self.max_undo_steps = max_undo_steps
        self.versions_dir = "versions"
        
        if not os.path.exists(self.versions_dir):
            os.makedirs(self.versions_dir)
            
    def save_state_to_undo(self, tree_dict):
        """Guarda el estado actual en la pila de Undo."""
        if tree_dict is None:
            return
            
        # Hacemos una copia profunda porsiaca
        state = copy.deepcopy(tree_dict)
        self.undo_stack.append(state)
        
        # Mantener límite de memoria
        if len(self.undo_stack) > self.max_undo_steps:
             self.undo_stack.pop(0)
             
    def can_undo(self):
        return len(self.undo_stack) > 0
        
    def pop_undo_state(self):
        """Extrae el último estado para deshacer la acción."""
        if self.can_undo():
            return self.undo_stack.pop()
        return None
        
    def save_version(self, tree_dict, version_name):
        """Guarda una versión en disco con el nombre especificado."""
        if tree_dict is None:
            raise ValueError("No se puede guardar un árbol vacío.")
            
        # Limpiar nombre
        safe_name = "".join([c for c in version_name if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        filename = f"{safe_name.replace(' ', '_')}.json"
        filepath = os.path.join(self.versions_dir, filename)
        
        data = {
            "version_name": version_name,
            "timestamp": datetime.now().isoformat(),
            "tree": tree_dict
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        return filepath
        
    def list_versions(self):
        """Lista las versiones guardadas en disco."""
        versions = []
        for filename in os.listdir(self.versions_dir):
            if filename.endswith(".json"):
                 filepath = os.path.join(self.versions_dir, filename)
                 try:
                     with open(filepath, 'r', encoding='utf-8') as f:
                         data = json.load(f)
                         versions.append({
                             "filename": filename,
                             "name": data.get("version_name", filename),
                             "timestamp": data.get("timestamp", "")
                         })
                 except:
                     pass
        # Ordenar por fecha desc
        versions.sort(key=lambda x: x["timestamp"], reverse=True)
        return versions
        
    def load_version(self, filename):
        """Carga una versión guardada."""
        filepath = os.path.join(self.versions_dir, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError("Versión no encontrada.")
            
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("tree")
