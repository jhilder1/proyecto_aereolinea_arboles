class FlightNode:
    """
    Representa un vuelo dentro del sistema SkyBalance.
    Actúa como nodo tanto para el BST como para el Árbol AVL.
    """
    def __init__(self, flight_id, base_price, passengers, promotion=0.0):
        # Propiedades de Estructura de Árbol
        self.value = flight_id  # Actúa como el ID o 'Key' para ordenar
        self.parent = None
        self.left_child = None
        self.right_child = None
        
        # Propiedades AVL
        self.height = 1 # Los nodos nuevos se añaden como hojas, altura 1.
        
        # Propiedades de Negocio (SkyBalance)
        self.base_price = base_price
        self.passengers = passengers
        self.promotion = promotion
        self.critical_depth_penalty = 0.0
        self.is_critical = False

    # --- Getters y Setters de la Estructura de Árbol ---
    def set_parent(self, parent_node):
        self.parent = parent_node

    def get_parent(self):
        return self.parent

    def set_left_child(self, left_child_node):
        self.left_child = left_child_node

    def get_left_child(self):
        return self.left_child

    def set_right_child(self, right_child_node):
        self.right_child = right_child_node

    def get_right_child(self):
        return self.right_child

    def get_value(self):
        return self.value

    # --- Reglas de Negocio ---
    def update_critical_status(self, depth, threshold, penalty_percentage=0.25):
        """
        Punto 6: Sistema de Penalización por Profundidad Crítica.
        Si la profundidad supera el umbral, se activa la bandera y se calcula penalización.
        """
        if depth > threshold:
            self.is_critical = True
            self.critical_depth_penalty = self.base_price * penalty_percentage
        else:
            self.is_critical = False
            self.critical_depth_penalty = 0.0

    def get_final_price(self):
        """Calcula el precio final aplicando promociones y penalizaciones."""
        # Rentabilidad = pasajeros × precioFinal – promoción (si aplica) + penalización (si aplica)
        # Asumimos que el precio final unitario es base + penalizacion - promo (simplificado).
        return self.base_price + self.critical_depth_penalty - self.promotion

    def get_profitability(self):
        """Punto 8: Cálculo de rentabilidad del vuelo."""
        final_price_per_passenger = self.get_final_price()
        return self.passengers * final_price_per_passenger
    
    def __str__(self):
        return f"FlightNode(ID:{self.value}, H:{self.height}, Price:{self.get_final_price()})"
