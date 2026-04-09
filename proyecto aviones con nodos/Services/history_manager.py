import copy
import json
import os
from datetime import datetime

class HistoryManager:
    """
    Gestiona el historial del árbol para permitir:
    - Ver la línea temporal completa (Time-Travel).
    - Viajar en el tiempo sin borrar pasos futuros.
    - Guardar versiones con nombres específicos en el sistema de archivos.
    """
    
    def __init__(self, max_undo_steps=50):
        self.timeline = [] 
        self.max_undo_steps = max_undo_steps
        self.versions_dir = "versions"
        
        if not os.path.exists(self.versions_dir):
            os.makedirs(self.versions_dir)
            
    def record_action(self, tree_dict, action_name="Operación Desconocida"):
        """Registra una acción en la línea de tiempo."""
        if tree_dict is None:
            return
            
        # Hacemos una copia profunda porsiaca
        state = copy.deepcopy(tree_dict)
        
        entry = {
            "action": action_name,
            "timestamp": datetime.now().isoformat(),
            "tree_state": state
        }
        
        self.timeline.append(entry)
        
        # Mantener límite de memoria
        if len(self.timeline) > self.max_undo_steps:
             self.timeline.pop(0)

    def get_timeline_summary(self):
        """Devuelve un resumen de todos los movimientos en el historial."""
        return [
            {
                "index": i, 
                "action": entry["action"], 
                "timestamp": entry["timestamp"]
            } 
            for i, entry in enumerate(self.timeline)
        ]
             
    def get_state_at(self, index):
        """Recupera el estado de un punto en el tiempo específico."""
        if 0 <= index < len(self.timeline):
            return copy.deepcopy(self.timeline[index]["tree_state"])
        return None

    # Mantenemos las compatibilidades pero referenciadas a timeline
    def save_state_to_undo(self, tree_dict):
        # Para compatibilidad con endpoints no actualizados
        self.record_action(tree_dict, "Acción Legacy")

    def can_undo(self):
        return len(self.timeline) > 1
        
    def pop_undo_state(self):
        """Extrae el penúltimo estado para deshacer la acción, truncando futuro."""
        if self.can_undo():
            self.timeline.pop() # Borramos el actual
            return copy.deepcopy(self.timeline[-1]["tree_state"])
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
