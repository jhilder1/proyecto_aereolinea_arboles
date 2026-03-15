from models.node import FlightNode

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
        """Carga la topología del árbol AVL desde JSON"""
        tree.root = self.build_tree_from_json(json_data)


    def build_tree_from_json(self, node_data):
        """
        Construye recursivamente una estructura de árbol a partir de JSON.
        """

        if node_data is None:
            return None

        node = self.create_flight_node(node_data)
        left_child_data = node_data.get("izquierda")
        right_child_data = node_data.get("derecha")

        left_child = self.build_tree_from_json(left_child_data)
        right_child = self.build_tree_from_json(right_child_data)
        node.set_left_child(left_child)
        node.set_right_child(right_child)
        
        if left_child:
            left_child.set_parent(node)

        if right_child:
            right_child.set_parent(node)

        
        node.height = 1 + max(
            left_child.height if left_child else 0, 
            right_child.height if right_child else 0
        )

        
        return node
    
    