from models.node import FlightNode
from models.avl_tree import AVL 

class FlightController:
    
    def create_flight_node(self, flight_data):
        """Crea un nodo de vuelo a partir de los datos proporcionados."""
        return FlightNode(
            flight_id=flight_data["codigo"],
            origin=flight_data["origen"],
            destination=flight_data["destino"],
            departure_time=flight_data["horaSalida"],
            base_price=flight_data["precioBase"],
            passengers=flight_data["pasajeros"],
            priority=flight_data["prioridad"],
            promotion=flight_data["promocion"],
            alert=flight_data["alerta"]
        )
        
    def insert_flights_into_tree(self, tree, flights):

        for flight in flights:

            node = self.create_flight_node(flight)

            tree.insert(node)
        
    
    def load_topology_tree(self, tree, json_data):
        """Carga la topología del árbol AVL desde un JSON."""
        for node_info in json_data:
            node = self.create_flight_node(node_info)
            tree.root = self.build_tree_from_json(json_data)

    
    
    