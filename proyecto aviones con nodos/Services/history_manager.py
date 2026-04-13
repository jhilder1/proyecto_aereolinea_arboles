import copy
import json
import os
from datetime import datetime

class HistoryManager:
    """
    Manages the tree's history to allow:
    - Viewing the complete timeline (Time-Travel).
    - Time traveling without deleting future steps.
    - Saving versions with specific names to the file system.
    """
    
    def __init__(self, max_undo_steps=50):
        self.timeline = [] 
        self.max_undo_steps = max_undo_steps
        self.versions_dir = "versions"
        
        if not os.path.exists(self.versions_dir):
            os.makedirs(self.versions_dir)
            
    def record_action(self, tree_dict, action_name="Operación Desconocida"):
        """Records an action on the timeline."""
        if tree_dict is None:
            return
            
        # Deep copy just in case
        state = copy.deepcopy(tree_dict)
        
        entry = {
            "action": action_name,
            "timestamp": datetime.now().isoformat(),
            "tree_state": state
        }
        
        self.timeline.append(entry)
        
        # Maintain memory limit
        if len(self.timeline) > self.max_undo_steps:
             self.timeline.pop(0)

    def get_timeline_summary(self):
        """Returns a summary of all history movements."""
        return [
            {
                "index": i, 
                "action": entry["action"], 
                "timestamp": entry["timestamp"]
            } 
            for i, entry in enumerate(self.timeline)
        ]
             
    def get_state_at(self, index):
        """Retrieves the state of a specific point in time."""
        if 0 <= index < len(self.timeline):
            return copy.deepcopy(self.timeline[index]["tree_state"])
        return None

    # We keep compatibility but referenced to the timeline
    def save_state_to_undo(self, tree_dict):
        # For compatibility with legacy endpoints not updated
        self.record_action(tree_dict, "Legacy Action")

    def can_undo(self):
        return len(self.timeline) > 1
        
    def pop_undo_state(self):
        """Extracts the penultimate state to undo the action, truncating the future."""
        if self.can_undo():
            self.timeline.pop() # Delete the current
            return copy.deepcopy(self.timeline[-1]["tree_state"])
        return None
        
    def save_version(self, tree_dict, version_name):
        """Saves a version to disk with the specified name."""
        if tree_dict is None:
            raise ValueError("No se puede guardar un árbol vacío.")
            
        # Clean name
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
        """Lists versions saved on disk."""
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
        # Sort by date desc
        versions.sort(key=lambda x: x["timestamp"], reverse=True)
        return versions
        
    def load_version(self, filename):
        """Loads a saved version."""
        filepath = os.path.join(self.versions_dir, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError("Versión no encontrada.")
            
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("tree")
