class Traversals:

    # ================================
    # BREADTH FIRST SEARCH (ANCHURA)
    # ================================

    @staticmethod
    def breadthFirstSearch(root):
        """Método para recorrido en anchura"""
        if root is None:
            raise Exception("El árbol está vacío.")
        else:
            return Traversals.__breadthFirstSearch(root)

    @staticmethod
    def __breadthFirstSearch(currentRoot):
        """Método para mostrar el recorrido en anchura"""
        queue = []
        result = []

        queue.append(currentRoot)

        while len(queue) > 0:
            currentRoot = queue.pop(0)

            result.append(currentRoot.get_value())

            if currentRoot.get_left_child() is not None:
                queue.append(currentRoot.get_left_child())

            if currentRoot.get_right_child() is not None:
                queue.append(currentRoot.get_right_child())

        return result


    # ================================
    # PRE ORDER
    # ================================

    @staticmethod
    def preOrderTraversal(root):
        """Método para recorrido en profundidad pre-order"""
        if root is None:
            raise Exception("El árbol está vacío.")
        else:
            return Traversals.__preOrderTraversal(root)

    @staticmethod
    def __preOrderTraversal(currentRoot):
        """Root - Left - Right"""

        print(currentRoot.get_value())

        if currentRoot.get_left_child() is not None:
            Traversals.__preOrderTraversal(currentRoot.get_left_child())

        if currentRoot.get_right_child() is not None:
            Traversals.__preOrderTraversal(currentRoot.get_right_child())


    # ================================
    # IN ORDER
    # ================================

    @staticmethod
    def inOrderTraversal(root):
        """Método para recorrido en profundidad in-order"""
        if root is None:
            raise Exception("El árbol está vacío.")
        else:
            return Traversals.__inOrderTraversal(root)

    @staticmethod
    def __inOrderTraversal(currentRoot):
        """Left - Root - Right"""

        if currentRoot.get_left_child() is not None:
            Traversals.__inOrderTraversal(currentRoot.get_left_child())

        print(currentRoot.get_value())

        if currentRoot.get_right_child() is not None:
            Traversals.__inOrderTraversal(currentRoot.get_right_child())


    # ================================
    # POST ORDER
    # ================================

    @staticmethod
    def posOrderTraversal(root):
        """Método para recorrido en profundidad pos-order"""
        if root is None:
            raise Exception("El árbol está vacío.")
        else:
            return Traversals.__posOrderTraversal(root)

    @staticmethod
    def __posOrderTraversal(currentRoot):
        """Left - Right - Root"""

        if currentRoot.get_left_child() is not None:
            Traversals.__posOrderTraversal(currentRoot.get_left_child())

        if currentRoot.get_right_child() is not None:
            Traversals.__posOrderTraversal(currentRoot.get_right_child())

        print(currentRoot.get_value())
