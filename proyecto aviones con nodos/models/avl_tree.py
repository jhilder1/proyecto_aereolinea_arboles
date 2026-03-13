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

    def search(self, value):
        """Método de búsqueda de un nodo con base en su valor"""
        if self.root is None:
            raise Exception("El árbol está vacío.")
        else:
            return self.__search(self.root, value)

    def __search(self, currentRoot, value):
        """Método para la búsqueda de manera recursiva"""
        # Si el valor coincide con el nodo actual, retornar el nodo
        if value == currentRoot.get_value():
            return currentRoot
        # Si el valor es mayor, buscar en el subárbol derecho
        if value > currentRoot.get_value():
            if currentRoot.get_right_child() is None:
                return None
            else:
                return self.__search(currentRoot.get_right_child(), value)
        # Si el valor es menor, buscar en el subárbol izquierdo
        else:
            if currentRoot.get_left_child() is None:
                return None
            else:
                return self.__search(currentRoot.get_left_child(), value)

    def delete(self, value):
        """Método para eliminar un nodo. Se deben considerar los 3 casos: no hoja, no con un hijo y nodo con 2 hijos"""
        # Verificar si el árbol tiene al menos la raíz
        if self.root is None:
            print("El árbol está vacío.")
        else:
            # Buscar el nodo con el valor
            node = self.search(value)
            # Si no se encuentra, mostrar mensaje de error
            if node is None:
                print(f"El nodo con valor {value} no existe en el árbol")
            else:
                # Eliminar el nodo
                self.__delete(node)

    def __delete(self, node):
        """Método para identificar el caso y eliminar el nodo"""
        # Identificar el caso de eliminación
        deletionCase = self.__identifyDeletionCase(node)
        # Ejecutar el caso correspondiente
        if deletionCase == 1:
            self.__deleteLeafNode(node)
        elif deletionCase == 2:
            self.__deleteNodeWithOneChild(node)
        elif deletionCase == 3:
            self.__deleteNodeWithTwoChildren(node)

    def __deleteNodeWithTwoChildren(self, node):
        """Método para eliminar un nodo que tiene dos hijos (caso 3)"""
        # Obtener el predecesor inorden
        predecessor = self.__getPredecessor(node)
        # Copiar el valor del predecesor al nodo actual
        node.set_value(predecessor.get_value())
        # Identificar el caso del predecesor y eliminarlo
        predecessorCase = self.__identifyDeletionCase(predecessor)
        if predecessorCase == 1:
            self.__deleteLeafNode(predecessor)
        else:
            self.__deleteNodeWithOneChild(predecessor)

    def __getPredecessor(self, node):
        """Método para obtener el predecesor inorden de un nodo. El predecesor es el mayor valor del subárbol izquierdo"""
        # Iniciar desde el hijo izquierdo
        current = node.get_left_child()
        # Avanzar hacia la derecha hasta el mayor valor
        while current.get_right_child() is not None:
            current = current.get_right_child()
        return current

    def __deleteNodeWithOneChild(self, node):
        """Método para eliminar un nodo que tiene un solo hijo (caso 2)"""
        # Obtener el hijo del nodo
        if node.get_left_child() is not None:
            childNode = node.get_left_child()
        else:
            childNode = node.get_right_child()

        # Obtener el padre del nodo
        parentNode = node.get_parent()

        # Si el nodo es la raíz, el hijo pasa a ser la nueva raíz
        if parentNode is None:
            self.root = childNode
            childNode.set_parent(None)
        else:
            # Verificar si es hijo izquierdo o derecho y ajustar referencias
            if parentNode.get_left_child() == node:
                parentNode.set_left_child(childNode)
            else:
                parentNode.set_right_child(childNode)
            childNode.set_parent(parentNode)

        # Limpiar referencias del nodo eliminado
        node.set_left_child(None)
        node.set_right_child(None)
        node.set_parent(None)

    def __deleteLeafNode(self, node):
        """Método para eliminar un nodo hoja (caso 1)"""
        # Si es la raíz, vaciar el árbol
        if node.get_value() == self.root.get_value():
            self.root = None
        else:
            # Obtener el padre y remover la referencia
            parentNode = node.get_parent()
            if node.get_value() < parentNode.get_value():
                parentNode.set_left_child(None)
            else:
                parentNode.set_right_child(None)
            node.set_parent(None)

    def __identifyDeletionCase(self, node):
        """Identificar los casos de eliminación: caso 1 cuando es nodo hoja, caso 2 cuando solo tiene un hijo, caso 3 cuando tiene los dos hijos"""
        # Asumir caso 2 inicialmente
        deletionCase = 2
        # Verificar si es hoja (caso 1)
        if node.get_left_child() is None and node.get_right_child() is None:
            deletionCase = 1
        # Verificar si tiene dos hijos (caso 3)
        elif node.get_left_child() is not None and node.get_right_child() is not None:
            deletionCase = 3
        return deletionCase

    def breadthFirstSearch(self):
        """Método para recorrido en anchura"""
        if self.root is None:
            raise Exception("El árbol está vacío.")
        else:
            return self.__breadthFirstSearch(self.root)

    def __breadthFirstSearch(self, currentRoot):
        """Método para mostrar el recorrido en anchura. Se obtiene una lista con los valores de los nodos recorridos"""
        # Inicializar cola y resultado
        queue = []
        result = []
        queue.append(currentRoot)
        # Mientras haya nodos en la cola
        while len(queue) > 0:
            # Desencolar el nodo actual
            currentRoot = queue.pop(0)
            # Agregar valor al resultado
            result.append(currentRoot.get_value())
            # Encolar hijos izquierdo y derecho si existen
            if currentRoot.get_left_child() is not None:
                queue.append(currentRoot.get_left_child())
            if currentRoot.get_right_child() is not None:
                queue.append(currentRoot.get_right_child())
        return result

    def preOrderTraversal(self):
        """Método para recorrido en profundidad pre-order"""
        if self.root is None:
            raise Exception("El árbol está vacío.")
        else:
            return self.__preOrderTraversal(self.root)

    def __preOrderTraversal(self, currentRoot):
        """Root - Left - Right"""
        # Imprimir valor del nodo actual
        print(currentRoot.get_value())
        # Recorrer subárbol izquierdo
        if currentRoot.get_left_child() is not None:
            self.__preOrderTraversal(currentRoot.get_left_child())
        # Recorrer subárbol derecho
        if currentRoot.get_right_child() is not None:
            self.__preOrderTraversal(currentRoot.get_right_child())

    def inOrderTraversal(self):
        """Método para recorrido en profundidad in-order"""
        if self.root is None:
            raise Exception("El árbol está vacío.")
        else:
            return self.__inOrderTraversal(self.root)

    def __inOrderTraversal(self, currentRoot):
        """Left - Root - Right"""
        # Recorrer subárbol izquierdo
        if currentRoot.get_left_child() is not None:
            self.__inOrderTraversal(currentRoot.get_left_child())
        # Imprimir valor del nodo actual
        print(currentRoot.get_value())
        # Recorrer subárbol derecho
        if currentRoot.get_right_child() is not None:
            self.__inOrderTraversal(currentRoot.get_right_child())

    def posOrderTraversal(self):
        """Método para recorrido en profundidad pos-order"""
        if self.root is None:
            raise Exception("El árbol está vacío.")
        else:
            return self.__posOrderTraversal(self.root)

    def __posOrderTraversal(self, currentRoot):
        """Left - Right - Root"""
        # Recorrer subárbol izquierdo
        if currentRoot.get_left_child() is not None:
            self.__posOrderTraversal(currentRoot.get_left_child())
        # Recorrer subárbol derecho
        if currentRoot.get_right_child() is not None:
            self.__posOrderTraversal(currentRoot.get_right_child())
        # Imprimir valor del nodo actual
        print(currentRoot.get_value())

    def calculateHeight(self, node):
        """Método para calcular la altura de un nodo"""
        if node is None:
            return -1
        else:
            return self.__calculateHeight(node)

    def __calculateHeight(self, currentRoot):
        """Método recursivo para calcular la altura de un nodo"""
        if currentRoot is None:
            return -1
        else:
            # Calcular altura del subárbol izquierdo
            leftHeight = self.__calculateHeight(currentRoot.get_left_child())
            # Calcular altura del subárbol derecho
            rightHeight = self.__calculateHeight(currentRoot.get_right_child())
            # Altura es 1 + máximo de las alturas de los hijos
            maxHeight = max(leftHeight, rightHeight)
            return 1 + maxHeight

    def print_tree(self):
        """Método para dibujar el árbol en forma de árbol"""
        if self.root is None:
            print("El árbol está vacío.")
        else:
            self.__print_tree(self.root, "", True)

    def __print_tree(self, node=None, prefix="", is_left=True):
        """Método para imprimir el árbol AVL"""
        if node is not None:
            # Imprimir subárbol derecho primero (para que aparezca arriba)
            if node.get_right_child():
                new_prefix = prefix + ("│   " if is_left else "    ")
                self.__print_tree(node.get_right_child(), new_prefix, False)

            # Imprimir el nodo actual
            connector = "└── " if is_left else "┌── "
            print(prefix + connector + str(node.get_value()))

            # Imprimir subárbol izquierdo
            if node.get_left_child():
                new_prefix = prefix + ("    " if is_left else "│   ")
                self.__print_tree(node.get_left_child(), new_prefix, True)

    def __checkBalance(self, node):
        """Método que verifica el balanceo de un árbol y si está desbalanceado ejecuta el proceso de balanceo"""
        # Obtener el padre del nodo actual
        parentNode = node.get_parent()
        # Si no hay padre, hemos llegado a la raíz
        if parentNode is None:
            return
        # Calcular factor de balance del padre
        bf = self.get_balance_factor(parentNode)
        # Si está desbalanceado, rebalancear
        if bf > 1 or bf < -1:
            self.__rebalance(parentNode, bf)
        # Continuar verificando hacia arriba
        self.__checkBalance(parentNode)

    def __rebalance(self, node, bf):
        """Método para balancear el árbol, identificando la dirección del desbalanceo con positivos por izquierda y negativos por derecha"""
        # Identificar el caso de rebalanceo
        rebalanceCase = self.__identifyRebalanceCase(node, bf)
        # Ejecutar la rotación correspondiente
        if rebalanceCase == "LL":
            self.__balanceLL(node)
        elif rebalanceCase == "RR":
            self.__balanceRR(node)
        elif rebalanceCase == "LR":
            self.__balanceLR(node)
        elif rebalanceCase == "RL":
            self.__balanceRL(node)

    def __balanceLR(self, topNode):
        """Método para el balanceo de tipo LR"""
        raise Exception("No implementado")

    def __balanceRL(self, topNode):
        """Método para el balanceo de tipo RL"""
        raise Exception("No implementado")

    def __balanceLL(self, topNode):
        """Método para el balanceo de tipo LL"""
        # Obtener hijo izquierdo del nodo superior
        middleNode = topNode.get_left_child()
        # Obtener padre del nodo superior
        topNodeParent = topNode.get_parent()
        # Obtener hijo derecho del nodo medio
        rightChildOfMiddle = middleNode.get_right_child()

        # Realizar rotación: middleNode pasa a ser padre de topNode
        middleNode.set_right_child(topNode)
        topNode.set_parent(middleNode)
        middleNode.set_parent(topNodeParent)

        # Ajustar referencias del padre
        if topNodeParent is None:
            self.root = middleNode
        else:
            if topNodeParent.get_left_child() == topNode:
                topNodeParent.set_left_child(middleNode)
            else:
                topNodeParent.set_right_child(middleNode)

        # Reasignar hijo derecho de topNode
        topNode.set_left_child(rightChildOfMiddle)
        if rightChildOfMiddle is not None:
            rightChildOfMiddle.set_parent(topNode)

    def __balanceRR(self, topNode):
        """Método para el balanceo de tipo RR"""
        # Obtener hijo derecho del nodo superior
        middleNode = topNode.get_right_child()
        # Obtener padre del nodo superior
        topNodeParent = topNode.get_parent()
        # Obtener hijo izquierdo del nodo medio
        leftChildOfMiddle = middleNode.get_left_child()

        # Realizar rotación: middleNode pasa a ser padre de topNode
        middleNode.set_left_child(topNode)
        topNode.set_parent(middleNode)
        middleNode.set_parent(topNodeParent)

        # Ajustar referencias del padre
        if topNodeParent is None:
            self.root = middleNode
        else:
            if topNodeParent.get_left_child() == topNode:
                topNodeParent.set_left_child(middleNode)
            else:
                topNodeParent.set_right_child(middleNode)

        # Reasignar hijo izquierdo de topNode
        topNode.set_right_child(leftChildOfMiddle)
        if leftChildOfMiddle is not None:
            leftChildOfMiddle.set_parent(topNode)

    def __identifyRebalanceCase(self, node, bf):
        """Método para identificar el caso de desbalanceo"""
        rebalanceCase = ""
        # Desbalanceo positivo (izquierda)
        if bf > 0:
            childBf = self.get_balance_factor(node.get_left_child())
            if childBf > 0:
                rebalanceCase = "LL"
            else:
                rebalanceCase = "LR"
        # Desbalanceo negativo (derecha)
        else:
            childBf = self.get_balance_factor(node.get_right_child())
            if childBf > 0:
                rebalanceCase = "RL"
            else:
                rebalanceCase = "RR"
        return rebalanceCase
            
    

