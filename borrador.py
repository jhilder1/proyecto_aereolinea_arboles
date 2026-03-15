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
            
    

