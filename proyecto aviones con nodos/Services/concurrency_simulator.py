from queue import Queue
from models.node import FlightNode

class ConcurrencySimulator:
    """
    Simula flujos de inserciones simultáneas manejándolas
    en una Cola de Solicitudes pendientes.
    """
    
    def __init__(self):
        self.pending_queue = Queue()
        
    def enqueue_flight(self, flight_dict):
        """Añade un vuelo a la cola de pendientes."""
        self.pending_queue.put(flight_dict)
        return self.get_queue_size()
        
    def get_queue_size(self):
        return self.pending_queue.qsize()
        
    def get_pending_flights(self):
        """Retorna una lista con los elementos actuales de la cola (sin sacarlos)"""
        return list(self.pending_queue.queue)
        
    def process_next(self, tree, flight_controller):
        """
        Procesa (desencola) el siguiente vuelo y lo inserta en el árbol.
        Devuelve información sobre el nodo insertado y si generó rebalanceo crítico.
        """
        if self.pending_queue.empty():
            return None
            
        flight_dict = self.pending_queue.get()
        
        # Capturamos cuantas rotaciones había antes
        rotations_before = sum(tree.rotations_count.values())
        
        # Insertar
        node = flight_controller.create_flight_node(flight_dict)
        tree.insert(node)
        
        # Rotaciones después
        rotations_after = sum(tree.rotations_count.values())
        rotations_diff = rotations_after - rotations_before
        
        return {
            "flight_inserted": flight_dict["codigo"],
            "rotations_caused": rotations_diff,
            "conflict_alert": rotations_diff > 0 # Si hubo rotación, consideramos que hubo un impacto estructural
        }
        
    def clear_queue(self):
        with self.pending_queue.mutex:
            self.pending_queue.queue.clear()
