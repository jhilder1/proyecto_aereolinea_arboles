class Traversals:

    # ================================
    # BREADTH FIRST SEARCH
    # ================================

    @staticmethod
    def breadthFirstSearch(root):
        """Breadth-first search method"""
        if root is None:
            raise Exception("The tree is empty.")
        else:
            return Traversals.__breadthFirstSearch(root)

    @staticmethod
    def __breadthFirstSearch(currentRoot):
        """Method to display the breadth-first search"""
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
        results = []
        """Method for pre-order depth-first search"""
        if root is None:
            raise Exception("The tree is empty.")
        else:
            Traversals.__preOrderTraversal(root, results)
        return results

    @staticmethod
    def __preOrderTraversal(currentRoot, results):
        """Root - Left - Right"""
        
        results.append(currentRoot.get_value())

        if currentRoot.get_left_child() is not None:
            Traversals.__preOrderTraversal(currentRoot.get_left_child(), results)

        if currentRoot.get_right_child() is not None:
            Traversals.__preOrderTraversal(currentRoot.get_right_child(), results)

        return results


    # ================================
    # IN ORDER
    # ================================

    @staticmethod
    def inOrderTraversal(root):
        results = []
        """Method for in-order depth-first search"""
        if root is None:
            raise Exception("The tree is empty.")
        else:
            Traversals.__inOrderTraversal(root, results)
        return results

    @staticmethod
    def __inOrderTraversal(currentRoot, results):
        """Left - Root - Right"""

        

        if currentRoot.get_left_child() is not None:
            Traversals.__inOrderTraversal(currentRoot.get_left_child(), results)
        
        results.append(currentRoot.get_value())

        if currentRoot.get_right_child() is not None:
            Traversals.__inOrderTraversal(currentRoot.get_right_child(), results)

        return results

    # ================================
    # POST ORDER
    # ================================

    @staticmethod
    def posOrderTraversal(root):
        results = []
        """Method for post-order depth-first search"""
        if root is None:
            raise Exception("The tree is empty.")
        else:
            Traversals.__posOrderTraversal(root, results)
        return results

    @staticmethod
    def __posOrderTraversal(currentRoot, results):
        """Left - Right - Root"""

        
        if currentRoot.get_left_child() is not None:
            Traversals.__posOrderTraversal(currentRoot.get_left_child(), results)

        if currentRoot.get_right_child() is not None:
            Traversals.__posOrderTraversal(currentRoot.get_right_child(), results)
            
        results.append(currentRoot.get_value())
        return results
