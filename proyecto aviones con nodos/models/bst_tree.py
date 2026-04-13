from models.node import FlightNode

class BST:
    """Base Binary Search Tree.
    This tree will be used in parallel with the AVL to demonstrate the structural
    difference when there is no balancing in subsequent insertions.
    """
    def __init__(self):
        self.root = None

    def insert(self, node: FlightNode):
        """Inserts a node into the tree without applying balancing."""
        if self.root is None:
            self.root = node
        else:
            self._insert(self.root, node)

    def _insert(self, current_root: FlightNode, node: FlightNode):
        if node.get_value() == current_root.get_value():
            raise Exception(f"Flight with ID {node.get_value()} already exists.")
            
        elif node.get_value() > current_root.get_value():
            # Goes to the right
            if current_root.get_right_child() is None:
                current_root.set_right_child(node)
                node.set_parent(current_root)
            else:
                self._insert(current_root.get_right_child(), node)
                
        else:
            # Goes to the left
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
        """Breadth-First Search traversal."""
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
    
    ## Function to calculate the height of the tree
    
    def get_height(self, node: FlightNode = None):
        """Calculates the maximum height of the tree or a subtree (O(n) in simple BST)."""
        if node is None:
            if self.root is None:
                return 0
            node = self.root
            
        left_h = self.get_height(node.get_left_child()) if node.get_left_child() else 0
        right_h = self.get_height(node.get_right_child()) if node.get_right_child() else 0
        
        return 1 + max(left_h, right_h)

    def count_leaves(self, node: FlightNode = None):
        """Counts the number of leaves in the tree."""
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

    def export_to_dict(self):
        """Exports the complete tree to a dictionary for json visualization."""
        if not self.root:
            return None
        return self._export_node_to_dict(self.root)
        
    def _export_node_to_dict(self, node: FlightNode):
        if not node:
            return None
        data = node.to_dict()
        data["factor_balanceo"] = 0 # Not applicable in simple BST
        data["izquierdo"] = self._export_node_to_dict(node.get_left_child())
        data["derecho"] = self._export_node_to_dict(node.get_right_child())
        return data
