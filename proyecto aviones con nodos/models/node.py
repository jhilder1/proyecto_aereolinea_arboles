class FlightNode:
    """
    Representa un vuelo dentro del sistema SkyBalance.
    Actúa como nodo tanto para el BST como para el Árbol AVL.
    """
    def __init__(self, flight_id, origin, base_price, passengers, promotion=0.0, alert=False):
        # Propiedades de Estructura de Árbol
        self.value = flight_id  # Actúa como el ID o 'Key' para ordenar
        self.origin = origin
        self.parent = None
        self.left_child = None
        self.right_child = None
        self.promotion = promotion
        self.alert = alert
        
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
        # Si la promoción es un booleano (como en el JSON), lo manejamos como un descuento fijo temporal (ej. 10%) o 0 si false.
        promo_discount = (self.base_price * 0.1) if self.promotion else 0.0
        # Rentabilidad = pasajeros × precioFinal – promoción (si aplica) + penalización (si aplica)
        # Aquí simplificamos el get_final_price que ya debió haber calculado esto,
        # pero para ser fieles a la formula: pass * (base + pen) - promo
        return (self.passengers * (self.base_price + self.critical_depth_penalty)) - promo_discount
        
    def to_dict(self):
        """Exporta el nodo y todos sus hijos a un diccionario serializable JSON. (Punto 1.3)"""
        return {
            "codigo": self.value,
            "origen": self.origin,
            "precioBase": self.base_price,
            "precioFinal": self.get_final_price(),
            "pasajeros": self.passengers,
            "promocion": self.promotion,
            "alerta": self.alert,
            "altura": self.height,
            "factor_balanceo": 0, # Se calculará en el AVL al exportar
            "is_critical": self.is_critical,
            "penalizacion": self.critical_depth_penalty,
            "izquierdo": self.left_child.to_dict() if self.left_child else None,
            "derecho": self.right_child.to_dict() if self.right_child else None
        }

    def __str__(self):
        return f"FlightNode(ID:{self.value}, H:{self.height}, Price:{self.get_final_price()})"
