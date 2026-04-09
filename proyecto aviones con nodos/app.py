from fastapi import FastAPI, HTTPException, Body, Query
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

class TreeSession:
    def __init__(self):
        self.avl = AVL()
        self.bst = BST()
        self.controller = FlightController()
        self.history = HistoryManager()
        self.simulator = ConcurrencySimulator()
        
        self.critical_depth_threshold = 5 # Por defecto
        self.cancellation_count = 0
        
        # Guardar el estado inicial en el historial
        self.history.record_action(self.avl.export_to_dict(), "Sistema Inicializado")

class AppState:
    def __init__(self):
        self.sessions = { "Principal": TreeSession() }
        
    def get_session(self, tree_id: str) -> TreeSession:
        if not tree_id:
            tree_id = "Principal"
        if tree_id not in self.sessions:
            self.sessions[tree_id] = TreeSession()
        return self.sessions[tree_id]

state = AppState()

def _update_penalties(node, session, depth=1):
    if not node: return
    # Calculamos penalizaciones por profundidad
    node.update_critical_status(depth, session.critical_depth_threshold)
    _update_penalties(node.get_left_child(), session, depth + 1)
    _update_penalties(node.get_right_child(), session, depth + 1)

def _force_rebalance(node, session):
    if not node: return
    _force_rebalance(node.get_left_child(), session)
    _force_rebalance(node.get_right_child(), session)
    session.avl._rebalance_upwards(node)

@app.get("/api/status")
def get_status():
    return {"status": "ok", "message": "SkyBalance API is running"}

@app.get("/api/trees")
def list_trees():
    """Retorna los identificadores de los vuelos (árboles) actuales."""
    return {"trees": list(state.sessions.keys())}

@app.post("/api/trees/{tree_id}")
def create_tree(tree_id: str):
    state.get_session(tree_id)
    return {"message": f"Vuelo / Árbol '{tree_id}' inicializado."}

@app.get("/api/compare")
def compare_trees(tree_id: str = "Principal"):
    session = state.get_session(tree_id)
    avl_root = session.avl.root
    bst_root = session.bst.root

    return {
        "AVL": {
            "root": avl_root.get_value() if avl_root else None,
            "height": avl_root.height if avl_root else 0,
            "leaves": session.bst.count_leaves(avl_root)
        },
        "BST": {
            "root": bst_root.get_value() if bst_root else None,
            "height": session.bst.get_height(bst_root) if bst_root else 0,
            "leaves": session.bst.count_leaves(bst_root)
        }
    }

@app.post("/api/load-tree")
async def load_tree_from_json(tree_id: str = "Principal", data: dict = Body(...)):
    session = state.get_session(tree_id)
    session.history.record_action(session.avl.export_to_dict(), "Previo a cargar JSON")
    
    try:
        flights = load_insert_data(data)
        session.avl = AVL()
        session.bst = BST()
        
        for flight in flights:
            node_avl = session.controller.create_flight_node(flight)
            node_bst = session.controller.create_flight_node(flight)
            session.avl.insert(node_avl)
            session.bst.insert(node_bst)
            
        _update_penalties(session.avl.root, session)
        session.history.record_action(session.avl.export_to_dict(), "Cargar JSON (Inserción)")
        
        return {"message": "Árbol AVL y BST cargados mediante inserción masiva.", "type": "INSERCIÓN"}
    except ValueError:
        try:
            tree_data = load_topology_data(data)
            session.avl = AVL()
            session.bst = BST()
            session.controller.load_topology_tree(session.avl, tree_data)
            session.controller.load_topology_tree(session.bst, tree_data)
            
            _update_penalties(session.avl.root, session)
            session.history.record_action(session.avl.export_to_dict(), "Cargar JSON (Topología)")
            
            return {"message": "Árbol AVL cargado desde topología.", "type": "TOPOLOGÍA"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al procesar el JSON: {str(e)}")

@app.get("/api/tree")
def get_tree_state(tree_id: str = "Principal"):
    """Retorna la topología completa del árbol AVL, BST y métricas base."""
    session = state.get_session(tree_id)
    avl_dict = session.avl.export_to_dict()
    
    bfs = Traversals.breadthFirstSearch(session.avl.root) if session.avl.root else []
    in_order = Traversals.inOrderTraversal(session.avl.root) if session.avl.root else []
    pre_order = Traversals.preOrderTraversal(session.avl.root) if session.avl.root else []
    post_order = Traversals.posOrderTraversal(session.avl.root) if session.avl.root else []
    
    metrics = {
        "height": session.avl.root.height if session.avl.root else 0,
        "rotations": session.avl.rotations_count,
        "massive_cancellations": session.cancellation_count,
        "leaves": session.bst.count_leaves(session.avl.root)
    }
    
    return {
        "avl": avl_dict,
        "metrics": metrics,
        "stress_mode": session.avl.stress_mode,
        "traversals": {
            "bfs": bfs,
            "in_order": in_order,
            "pre_order": pre_order,
            "post_order": post_order
        }
    }

@app.get("/api/export")
def export_tree(tree_id: str = "Principal"):
    """Exporta el árbol completo con estructura jerárquica."""
    session = state.get_session(tree_id)
    try:
        tree_data = session.avl.export_to_dict()
        return {
            "tree": tree_data,
            "metadata": {
                "type": "AVL",
                "height": session.avl.root.height if session.avl.root else 0,
                "rotations": session.avl.rotations_count,
                "stress_mode": session.avl.stress_mode
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
def enqueue_flight(flight: FlightCreate, tree_id: str = "Principal"):
    session = state.get_session(tree_id)
    size = session.simulator.enqueue_flight(flight.dict())
    return {"message": "Vuelo encolado", "queue_size": size}

@app.post("/api/flights/process")
def process_next_flight(tree_id: str = "Principal"):
    session = state.get_session(tree_id)
    session.history.record_action(session.avl.export_to_dict(), "Previo a procesar cola")
    
    result = session.simulator.process_next(session.avl, session.controller)
    if not result:
        return {"message": "No hay vuelos pendientes", "processed": False}
        
    _update_penalties(session.avl.root, session)
    session.history.record_action(session.avl.export_to_dict(), "Vuelo de la cola procesado")
    
    return {"message": "Vuelo procesado", "processed": True, "result": result}

@app.post("/api/flights")
def create_flight(flight: FlightCreate, tree_id: str = "Principal"):
    session = state.get_session(tree_id)
    try:
        node_avl = session.controller.create_flight_node(flight.dict())
        node_bst = session.controller.create_flight_node(flight.dict())

        session.avl.insert(node_avl)
        session.bst.insert(node_bst)

        _update_penalties(session.avl.root, session)

        session.history.record_action(session.avl.export_to_dict(), f"Crear vuelo {flight.codigo}")

        return {
            "message": "Vuelo creado correctamente",
            "codigo": flight.codigo
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/flights/{codigo}")
def modify_flight(codigo: str, cascade: bool = False, tree_id: str = "Principal"):
    session = state.get_session(tree_id)
    
    if cascade:
        node = session.avl.search(codigo)
        if not node:
            raise HTTPException(status_code=404, detail="No encontrado")
        session.cancellation_count += 1
        targets = Traversals.posOrderTraversal(node)
        for t in targets:
            session.avl.delete(t)
            
        session.history.record_action(session.avl.export_to_dict(), f"Cancelación masiva subrama {codigo}")
        return {"message": "Vuelo y descendientes cancelados"}
    else:
        try:
            session.avl.delete(codigo)
            session.history.record_action(session.avl.export_to_dict(), f"Eliminación {codigo}")
            return {"message": f"Nodo {codigo} eliminado"}
        except Exception as e:
             raise HTTPException(status_code=400, detail=str(e))

class ConfigUpdate(BaseModel):
    stress_mode: bool
    
class DepthUpdate(BaseModel):
    depth_threshold: int

@app.post("/api/depth")
def update_depth(config: DepthUpdate, tree_id: str = "Principal"):
    session = state.get_session(tree_id)
    
    session.history.save_state_to_undo(session.avl.export_to_dict())
    
    session.critical_depth_threshold = config.depth_threshold
    
    _update_penalties(session.avl.root, session)
    
    return {"message": "Profundidad crítica actualizada"}  

@app.post("/api/mode")
def update_mode(config: ConfigUpdate, tree_id: str = "Principal"):
    session = state.get_session(tree_id)
    
    was_stress = session.avl.stress_mode
    session.avl.stress_mode = config.stress_mode
    ##session.critical_depth_threshold = config.depth_threshold
    
    msg = "Configuración actualizada"
    if was_stress and not config.stress_mode:
        _force_rebalance(session.avl.root, session)
        msg = "Árbol rebalanceado forzosamente. Modo estrés desactivado."
        
    _update_penalties(session.avl.root, session)
    session.history.record_action(session.avl.export_to_dict(), "Cambió Modo Estrés")
    return {"message": msg}

@app.get("/api/tree/audit")
def audit_tree(tree_id: str = "Principal"):
    session = state.get_session(tree_id)
    if not session.avl.stress_mode:
        return {"message": "La auditoría solo está disponible en modo estrés.", "audit_valid": True}
        
    report = []
    def check_audit(node):
        if not node: return
        check_audit(node.get_left_child())
        bf = session.avl.get_balance_factor(node)
        if abs(bf) > 1:
           report.append({
               "codigo": node.value,
               "error": f"Factor de balanceo inváldo: {bf}",
               "altura": node.height
           })
        check_audit(node.get_right_child())

    check_audit(session.avl.root)
    return {
        "status": "inconsistente" if len(report) > 0 else "balanceado",
        "inconsistencies": report
    }

# HISTORY & TIME TRAVEL ENDPOINTS
@app.get("/api/history/{tree_id}/timeline")
def get_timeline(tree_id: str):
    session = state.get_session(tree_id)
    return {"timeline": session.history.get_timeline_summary()}

@app.post("/api/history/{tree_id}/travel/{index}")
def history_travel(tree_id: str, index: int):
    session = state.get_session(tree_id)
    tree_state = session.history.get_state_at(index)
    
    if not tree_state and tree_state != {}:  # tree state puede ser {}, pero None es un fallo
         # Ojo que si el arbol está vacío se serializa a {}, no a None en nuestro model
        if tree_state is None:
            raise HTTPException(status_code=404, detail="Índice no encontrado")
        
    session.avl = AVL()
    if tree_state:
        session.controller.load_topology_tree(session.avl, tree_state)
    _update_penalties(session.avl.root, session)
    
    # Viajamos sin alterar futuro. Solo loggeamos a dónde fuimos al final del tape temporal
    session.history.record_action(session.avl.export_to_dict(), f"Viaje en el Tiempo a index: {index}")
    
    return {"message": f"Se viajó en el tiempo exitosamente al evento {index}"}

@app.post("/api/history/undo")
def undo_action(tree_id: str = "Principal"):
    session = state.get_session(tree_id)
    if not session.history.can_undo():
         return {"message": "No hay acciones para deshacer", "undo": False}
         
    prev_state = session.history.pop_undo_state()
    session.avl = AVL()
    if prev_state:
        session.controller.load_topology_tree(session.avl, prev_state)
    _update_penalties(session.avl.root, session)
    
    return {"message": "Acción deshecha con éxito", "undo": True}

class VersionSave(BaseModel):
    name: str

@app.post("/api/versions/save")
def save_version(data: VersionSave, tree_id: str = "Principal"):
    session = state.get_session(tree_id)
    try:
        current_state = session.avl.export_to_dict()
        filepath = session.history.save_version(current_state, data.name)
        return {"message": f"Versión guardada como {data.name}", "path": filepath}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/versions")
def list_versions(tree_id: str = "Principal"):
    session = state.get_session(tree_id)
    return session.history.list_versions()

@app.post("/api/versions/load/{filename}")
def load_version(filename: str, tree_id: str = "Principal"):
    session = state.get_session(tree_id)
    try:
        tree_state = session.history.load_version(filename)
        session.avl = AVL()
        session.controller.load_topology_tree(session.avl, tree_state)
        _update_penalties(session.avl.root, session)
        session.history.record_action(session.avl.export_to_dict(), f"Versión Cargada: {filename}")
        return {"message": f"Versión {filename} cargada con éxito"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/flights/optimize/economic")
def delete_lowest_profitability(tree_id: str = "Principal"):
    session = state.get_session(tree_id)
    if not session.avl.root:
        return {"message": "El árbol está vacío."}
        
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

    evaluate_node(session.avl.root, 0)
    
    if best_candidate:
        codigo = best_candidate["node"].value
        prof_val = best_candidate["node"].get_profitability()
        session.cancellation_count += 1
        targets = Traversals.posOrderTraversal(best_candidate["node"])
        for t in targets:
            session.avl.delete(t)
            
        session.history.record_action(session.avl.export_to_dict(), f"Optimización Económica ({codigo})")
        return {"message": f"Vuelo {codigo} eliminado por baja rentabilidad ({prof_val}). Sub-rama eliminada."}
    
    return {"message": "No se pudo determinar candidato"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
