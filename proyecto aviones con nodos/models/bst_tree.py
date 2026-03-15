from models.node import FlightNode

class BST:
    """Árbol Binario de Búsqueda Base.
    Este árbol se usará en paralelo con el AVL para demostrar la diferencia
    estructural cuando no hay balanceo en inserciones subsecuentes.
    """
    def __init__(self):
        self.root = None

    def insert(self, node: FlightNode):
        """Inserta un nodo en el árbol sin aplicar balanceo."""
        if self.root is None:
            self.root = node
        else:
            self._insert(self.root, node)

    def _insert(self, current_root: FlightNode, node: FlightNode):
        if node.get_value() == current_root.get_value():
            raise Exception(f"El vuelo con ID {node.get_value()} ya existe.")
            
        elif node.get_value() > current_root.get_value():
            # Va hacia la derecha
            if current_root.get_right_child() is None:
                current_root.set_right_child(node)
                node.set_parent(current_root)
            else:
                self._insert(current_root.get_right_child(), node)
                
        else:
            # Va hacia la izquierda
            if current_root.get_left_child() is None:
                current_root.set_left_child(node)
                node.set_parent(current_root)
            else:
                self._insert(current_root.get_left_child(), node)

    def search(self, value):
        if self.root is None:
            return None
        return self._search(self.root, value)

    def _search(self, current_root: FlightNode, value):
        if current_root is None or current_root.get_value() == value:
            return current_root
            
        if value > current_root.get_value():
            return self._search(current_root.get_right_child(), value)
        else:
            return self._search(current_root.get_left_child(), value)

    def bread_first_search(self):
        """Recorrido en anchura."""
        if self.root is None:
            return []
            
        queue = [self.root]
        result = []
        
        while queue:
            current = queue.pop(0)
            result.append(current.get_value())
            
            if current.get_left_child():
                queue.append(current.get_left_child())
            if current.get_right_child():
                queue.append(current.get_right_child())
                
        return result
    
    ##Funcion para calcular la altura del arbol
    
    def get_height(self, node: FlightNode = None):
        """Calcula la altura máxima del árbol o de un subárbol (O(n) en BST simple)."""
        if node is None:
            if self.root is None:
                return 0
            node = self.root
            
        left_h = self.get_height(node.get_left_child()) if node.get_left_child() else 0
        right_h = self.get_height(node.get_right_child()) if node.get_right_child() else 0
        
        return 1 + max(left_h, right_h)

    def count_leaves(self, node: FlightNode = None):
        """Cuenta la cantidad de hojas en el árbol."""
        if node is None:
            if self.root is None:
                return 0
            node = self.root
            
        if node.get_left_child() is None and node.get_right_child() is None:
            return 1
            
        leaves = 0
        if node.get_left_child():
            leaves += self.count_leaves(node.get_left_child())
        if node.get_right_child():
            leaves += self.count_leaves(node.get_right_child())
            
        return leaves
