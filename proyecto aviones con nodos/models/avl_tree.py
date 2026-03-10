from models.node import FlightNode
from models.bst_tree import BST

class AVL(BST):
    """
    Árbol AVL (Adelson-Velsky y Landis) que hereda de BST.
    Garantiza una altura O(log n) mediante el rebalanceo automático.
    Se utiliza FlightNode como estructura de datos.
    """
    def __init__(self):
        super().__init__()
        self.stress_mode = False
        self.rotations_count = {
            'single_left': 0,
            'single_right': 0,
            'double_left': 0,
            'double_right': 0
        }

    def get_height_node(self, node: FlightNode):
        if not node:
            return 0
        return node.height

    def get_balance_factor(self, node: FlightNode):
        if not node:
            return 0
        return self.get_height_node(node.get_left_child()) - self.get_height_node(node.get_right_child())

    def _update_height(self, node: FlightNode):
        if node:
            node.height = 1 + max(self.get_height_node(node.get_left_child()),
                                  self.get_height_node(node.get_right_child()))

    def rotate_right(self, y: FlightNode):
        """
        Rotación Simple a la Derecha
            y                               x
           / \                            /   \
          x   T3      ----->             T1     y
         / \                                   / \
        T1  T2                                T2  T3
        """
        x = y.get_left_child()
        T2 = x.get_right_child()

        # Realizar rotación
        x.set_right_child(y)
        y.set_left_child(T2)

        # Actualizar padres
        x.set_parent(y.get_parent())
        y.set_parent(x)
        if T2:
            T2.set_parent(y)

        # Si 'y' era la raíz, 'x' pasa a ser la nueva raíz
        if x.get_parent() is None:
            self.root = x
        elif x.get_parent().get_left_child() == y:
            x.get_parent().set_left_child(x)
        else:
            x.get_parent().set_right_child(x)

        # Actualizar alturas
        self._update_height(y)
        self._update_height(x)

        self.rotations_count['single_right'] += 1
        return x

    def rotate_left(self, x: FlightNode):
        """
        Rotación Simple a la Izquierda
          x                               y
         / \                            /   \
        T1  y      ----->              x     T3
           / \                        / \
          T2  T3                     T1  T2
        """
        y = x.get_right_child()
        T2 = y.get_left_child()

        # Realizar rotación
        y.set_left_child(x)
        x.set_right_child(T2)

        # Actualizar padres
        y.set_parent(x.get_parent())
        x.set_parent(y)
        if T2:
            T2.set_parent(x)

        # Si 'x' era la raíz, 'y' pasa a ser la nueva raíz
        if y.get_parent() is None:
            self.root = y
        elif y.get_parent().get_left_child() == x:
            y.get_parent().set_left_child(y)
        else:
            y.get_parent().set_right_child(y)

        # Actualizar alturas
        self._update_height(x)
        self._update_height(y)

        self.rotations_count['single_left'] += 1
        return y

    def __rotateLeftRight(self, topNode):
        self.rotate_left(topNode.get_left_child())
        result = self.rotate_right(topNode)
        self.rotations_count['double_left'] += 1
        return result
        
    def __rotateRightLeft(self, topNode):
        self.rotate_right(topNode.get_right_child())
        result = self.rotate_left(topNode)
        self.rotations_count['double_right'] += 1
        return result

    def insert(self, node: FlightNode):
        """
        Sobrescribe el insert de BST para aplicar balanceo AVL opcionalmente.
        """
        if self.root is None:
            self.root = node
            return

        # 1. Inserción normal de BST
        super()._insert(self.root, node)
        
        # 2. Rebalanceo (si no estamos en modo estrés)
        if not self.stress_mode:
            self._rebalance_upwards(node)
        else:
            # En modo estrés el árbol se deforma, pero igual debemos actualizar
            # la altura del nodo modificado y sus ancestros para métricas futuras.
            self._update_heights_upwards(node)

    def _update_heights_upwards(self, node: FlightNode):
        """Actualiza la propiedad height hacia arriba desde el nodo actual."""
        current = node
        while current is not None:
            self._update_height(current)
            current = current.get_parent()

    def _rebalance_upwards(self, node: FlightNode):
        """Recorre hacia arriba verificando el factor de balanceo y rotando."""
        current = node
        while current is not None:
            self._update_height(current)
            balance = self.get_balance_factor(current)

            # Caso 1: Izquierda - Izquierda (LL)
            if balance > 1 and self.get_balance_factor(current.get_left_child()) >= 0:
                current = self.rotate_right(current)
            
            # Caso 2: Derecha - Derecha (RR)
            elif balance < -1 and self.get_balance_factor(current.get_right_child()) <= 0:
                current = self.rotate_left(current)
            
            # Caso 3: Izquierda - Derecha (LR)
            elif balance > 1 and self.get_balance_factor(current.get_left_child()) < 0:
                current = self.__rotateLeftRight(current)
            
            # Caso 4: Derecha - Izquierda (RL)
            elif balance < -1 and self.get_balance_factor(current.get_right_child()) > 0:
                current = self.__rotateRightLeft(current)
                
            current = current.get_parent()
            
    

