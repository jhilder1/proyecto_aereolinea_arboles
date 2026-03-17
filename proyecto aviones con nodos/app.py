from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# Importar modelos y servicios
from models.avl_tree import AVL
from models.bst_tree import BST
from models.traversals import Traversals

from controller.flight_controller import FlightController
from Services.history_manager import HistoryManager
from Services.concurrency_simulator import ConcurrencySimulator
from utils.json_loader import load_insert_data, load_topology_data
from fastapi.middleware.cors import CORSMiddleware

# Instancia de FastAPI
app = FastAPI(title="SkyBalance Airline API")

# Habilitar CORS para el frontend en React (dev server puertos típicos de Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estado Global del backend (Singleton en memoria)
class AppState:
    def __init__(self):
        self.avl = AVL()
        self.bst = BST()
        self.controller = FlightController()
        self.history = HistoryManager()
        self.simulator = ConcurrencySimulator()
        
        self.critical_depth_threshold = 5 # Por defecto
        self.cancellation_count = 0

state = AppState()

# ==========================================
# RUTAS DE LA API
# ==========================================

@app.get("/api/status")
def get_status():
    return {"status": "ok", "message": "SkyBalance API is running"}

@app.post("/api/load-tree")
async def load_tree_from_json(data: dict = Body(...)):
    """
    Recibe el JSON enviado desde el Frontend y lo inyecta en el árbol.
    """
    try:
        flights = load_insert_data(data)
        # Modo INSERCIÓN
        state.avl = AVL()
        state.bst = BST()
        
        for flight in flights:
            node_avl = state.controller.create_flight_node(flight)
            node_bst = state.controller.create_flight_node(flight)
            state.avl.insert(node_avl)
            state.bst.insert(node_bst)
            
        # Actualizamos penalizaciones después de insertar
        _update_penalties(state.avl.root)
        
        return {"message": "Árbol AVL y BST cargados mediante inserción masiva.", "type": "INSERCIÓN"}
    except ValueError:
        try:
            tree_data = load_topology_data(data)
            # Modo TOPOLOGÍA
            state.avl = AVL()
            state.bst = BST() # En topologia solo cargamos AVL o ambos si se quiere (pero asuminos AVL)
            state.controller.load_topology_tree(state.avl, tree_data)
            
            _update_penalties(state.avl.root)
            
            return {"message": "Árbol AVL cargado desde topología.", "type": "TOPOLOGÍA"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al procesar el JSON: {str(e)}")

def _update_penalties(node):
    if not node: return
    # Calculamos penalizaciones por profundidad
    node.update_critical_status(node.height, state.critical_depth_threshold)
    _update_penalties(node.get_left_child())
    _update_penalties(node.get_right_child())

@app.get("/api/tree")
def get_tree_state():
    """Retorna la topología completa del árbol AVL, BST y métricas base."""
    avl_dict = state.avl.export_to_dict()
    
    # Recorridos
    bfs = Traversals.breadthFirstSearch(state.avl.root) if state.avl.root else []
    in_order = Traversals.inOrderTraversal(state.avl.root) if state.avl.root else []
    pre_order = Traversals.preOrderTraversal(state.avl.root) if state.avl.root else []
    post_order = Traversals.posOrderTraversal(state.avl.root) if state.avl.root else []
    
    metrics = {
        "height": state.avl.root.height if state.avl.root else 0,
        "rotations": state.avl.rotations_count,
        "massive_cancellations": state.cancellation_count,
        "leaves": state.bst.count_leaves(state.avl.root) # Usando count_leaves prestado del BST que sirve para nodos en general
    }
    
    return {
        "avl": avl_dict,
        "metrics": metrics,
        "stress_mode": state.avl.stress_mode,
        "traversals": {
            "bfs": bfs,
            "in_order": in_order,
            "pre_order": pre_order,
            "post_order": post_order
        }
    }

class FlightCreate(BaseModel):
    codigo: str
    origen: str
    destino: str = ""
    horaSalida: str = ""
    precioBase: float
    pasajeros: int
    prioridad: int = 1
    promocion: bool = False
    alerta: bool = False

@app.post("/api/flights/enqueue")
def enqueue_flight(flight: FlightCreate):
    size = state.simulator.enqueue_flight(flight.dict())
    return {"message": "Vuelo encolado", "queue_size": size}

@app.post("/api/flights/process")
def process_next_flight():
    # Save for undo
    state.history.save_state_to_undo(state.avl.export_to_dict())
    
    result = state.simulator.process_next(state.avl, state.controller)
    if not result:
        return {"message": "No hay vuelos pendientes", "processed": False}
        
    _update_penalties(state.avl.root)
    return {"message": "Vuelo procesado", "processed": True, "result": result}

@app.delete("/api/flights/{codigo}")
def modify_flight(codigo: str, cascade: bool = False):
    """Punto 1.2: Eliminar un nodo (cascade=false) o Cancelar vuelo con descendencia (cascade=true)"""
    state.history.save_state_to_undo(state.avl.export_to_dict())
    
    if cascade:
        # Cancelación Masiva: eliminar nodo y SUBRAMA
        node = state.avl.search(codigo)
        if not node:
            raise HTTPException(status_code=404, detail="No encontrado")
        state.cancellation_count += 1
        # La eliminación en cascada en AVL puede ser emulada eliminando en postórden la subrama,
        # o cortando la referencia en el padre del nodo. Para mantener AVL:
        targets = Traversals.posOrderTraversal(node)
        for t in targets:
            state.avl.delete(t)
            
        return {"message": "Vuelo y todos sus descendientes cancelados masivamente"}
    else:
        # Eliminacion Normal AVL
        try:
            state.avl.delete(codigo)
            return {"message": f"Nodo {codigo} eliminado"}
        except Exception as e:
             raise HTTPException(status_code=400, detail=str(e))

class ConfigUpdate(BaseModel):
    stress_mode: bool
    depth_threshold: int

@app.post("/api/mode")
def update_mode(config: ConfigUpdate):
    state.history.save_state_to_undo(state.avl.export_to_dict())
    
    # Comprobamos si salimos del modo estrés a global
    was_stress = state.avl.stress_mode
    state.avl.stress_mode = config.stress_mode
    state.critical_depth_threshold = config.depth_threshold
    
    msg = "Configuración actualizada"
    if was_stress and not config.stress_mode:
        # Salida del modo estrés: Reparación en cascada
        # (Idealmente se llamara un método de repair() recorriendo posOrder)
        # Para forzar esto, actualizaremos rebalanceo desde hojas
        _force_rebalance(state.avl.root)
        msg = "Árbol rebalanceado forzosamente. Modo estrés desactivado."
        
    _update_penalties(state.avl.root)
    return {"message": msg}

def _force_rebalance(node):
    if not node: return
    _force_rebalance(node.get_left_child())
    _force_rebalance(node.get_right_child())
    state.avl._rebalance_upwards(node)

@app.get("/api/tree/audit")
def audit_tree():
    """Punto 7: Sistema de Auditoría (reporte detallado)."""
    if not state.avl.stress_mode:
        return {"message": "La auditoría solo está disponible en modo estrés.", "audit_valid": True}
        
    report = []
    
    def check_audit(node):
        if not node: return
        check_audit(node.get_left_child())
        
        bf = state.avl.get_balance_factor(node)
        status = abs(bf) <= 1
        
        if not status:
           report.append({
               "codigo": node.value,
               "error": f"Factor de balanceo inváldo: {bf}",
               "altura": node.height
           })
           
        check_audit(node.get_right_child())

    check_audit(state.avl.root)
    
    return {
        "status": "inconsistente" if len(report) > 0 else "balanceado",
        "inconsistencies": report
    }

@app.post("/api/history/undo")
def undo_action():
    if not state.history.can_undo():
         return {"message": "No hay acciones para deshacer", "undo": False}
         
    prev_state = state.history.pop_undo_state()
    # Reconstrucción basica del arbol a partir del state via topology
    state.avl = AVL()
    state.controller.load_topology_tree(state.avl, prev_state)
    _update_penalties(state.avl.root)
    
    return {"message": "Acción deshecha con éxito", "undo": True}

class VersionSave(BaseModel):
    name: str

@app.post("/api/versions/save")
def save_version(data: VersionSave):
    try:
        current_state = state.avl.export_to_dict()
        filepath = state.history.save_version(current_state, data.name)
        return {"message": f"Versión guardada como {data.name}", "path": filepath}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/versions")
def list_versions():
    return state.history.list_versions()

@app.post("/api/versions/load/{filename}")
def load_version(filename: str):
    try:
        tree_state = state.history.load_version(filename)
        state.avl = AVL()
        state.controller.load_topology_tree(state.avl, tree_state)
        _update_penalties(state.avl.root)
        return {"message": f"Versión {filename} cargada con éxito"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/flights/optimize/economic")
def delete_lowest_profitability():
    """Punto 8: Eliminar Nodo de Menor Rentabilidad"""
    if not state.avl.root:
        return {"message": "El árbol está vacío."}
        
    state.history.save_state_to_undo(state.avl.export_to_dict())
    
    # 1. Encontrar menor rentabilidad
    # Criterios: Menor rentabilidad -> Más lejano a la raíz (mayor height/prof) -> Mayor string ID
    best_candidate = None
    
    def evaluate_node(node, depth):
        nonlocal best_candidate
        if not node: return
        
        prof = node.get_profitability()
        # Evaluamos
        is_better = False
        if not best_candidate:
            is_better = True
        else:
            cand_prof = best_candidate["node"].get_profitability()
            if prof < cand_prof:
                is_better = True
            elif prof == cand_prof:
                if depth > best_candidate["depth"]:
                    is_better = True
                elif depth == best_candidate["depth"]:
                    if node.value > best_candidate["node"].value:
                         is_better = True
                         
        if is_better:
            best_candidate = {"node": node, "depth": depth}
            
        evaluate_node(node.get_left_child(), depth + 1)
        evaluate_node(node.get_right_child(), depth + 1)

    evaluate_node(state.avl.root, 0)
    
    if best_candidate:
        codigo = best_candidate["node"].value
        prof_val = best_candidate["node"].get_profitability()
        # 3. Cancelar subrama. (Impacta a toda la descendencia)
        state.cancellation_count += 1
        targets = Traversals.posOrderTraversal(best_candidate["node"])
        for t in targets:
            state.avl.delete(t)
            
        return {"message": f"Vuelo {codigo} eliminado por baja rentabilidad ({prof_val}). Sub-rama eliminada."}
    
    return {"message": "No se pudo determinar candidato"}


# Para levantar el servidor al ejecutar el archivo:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
