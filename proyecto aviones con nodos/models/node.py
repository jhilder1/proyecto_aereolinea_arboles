class FlightNode:
    """
    Represents a flight within the SkyBalance system.
    Acts as a node for both the BST and the AVL Tree.
    """
    def __init__(self, flight_id, origin, base_price, passengers, promotion=0.0, alert=False):
        # Tree Structure Properties
        self.value = flight_id  # Acts as the ID or 'Key' for ordering
        self.origin = origin
        self.parent = None
        self.left_child = None
        self.right_child = None
        self.promotion = promotion
        self.alert = alert
        ##self.depth = 0  # For tracking depth in the tree, useful for penalties.
        
        # AVL Properties
        self.height = 1 # New nodes are added as leaves, height 1.
        
        # Business Properties (SkyBalance)
        self.base_price = base_price
        self.passengers = passengers
        self.promotion = promotion
        self.critical_depth_penalty = 0.0
        self.is_critical = False

    # --- Tree Structure Getters and Setters ---
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

    # --- Business Rules ---
    def update_critical_status(self, depth, threshold, penalty_percentage=0.25):
        """
        Point 6: Critical Depth Penalty System.
        If depth exceeds the threshold, the flag is activated and penalty is calculated.
        """
        if depth > threshold:
            self.is_critical = True
            self.critical_depth_penalty = self.base_price * penalty_percentage
        else:
            self.is_critical = False
            self.critical_depth_penalty = 0.0

    def get_final_price(self):
        """Calculates the final price applying promotions and penalties."""
        # Profitability = passengers × final_price - promotion (if applicable) + penalty (if applicable)
        # We assume the unit final price is base + penalty - promo (simplified).
        return self.base_price + self.critical_depth_penalty - self.promotion

    def get_profitability(self):
        """Point 8: Calculation of flight profitability."""
        final_price_per_passenger = self.get_final_price()
        # If the promotion is a boolean (like in the JSON), we handle it as a fixed temporary discount (e.g. 10%) or 0 if false.
        promo_discount = (self.base_price * 0.1) if self.promotion else 0.0
        # Profitability = passengers × final_price - promotion (if applicable) + penalty (if applicable)
        # Here we simplify get_final_price which should have already calculated this,
        # but to be faithful to the formula: pass * (base + pen) - promo
        return (self.passengers * (self.base_price + self.critical_depth_penalty)) - promo_discount
        
    def to_dict(self):
        """Exports the node and all its children to a JSON serializable dictionary. (Point 1.3)"""
        return {
            "codigo": self.value,
            "origen": self.origin,
            "precioBase": self.base_price,
            "precioFinal": self.get_final_price(),
            "pasajeros": self.passengers,
            "promocion": self.promotion,
            "alerta": self.alert,
            "altura": self.height,
            "factor_balanceo": 0, # Will be calculated in the AVL when exporting
            "is_critical": self.is_critical,
            "penalizacion": self.critical_depth_penalty,
            
        }

    def __str__(self):
        return f"FlightNode(ID:{self.value}, H:{self.height}, Price:{self.get_final_price()})"
        
