from models.node import FlightNode


class Rotations:
    """
    Utility class that contains all the rotations of the AVL tree.

    Separated from the main tree to improve code modularity.
    Each method receives the tree and the node where the rotation will be performed.
    """

    @staticmethod
    def rotate_right(tree, y: FlightNode):
        """
        Single right rotation (LL).

                y                       x
               / \                    /   \
              x   T3      ---->      T1    y
             / \                         / \
            T1  T2                      T2  T3

        This rotation is applied when the left subtree
        is unbalanced to the left.
        """

        x = y.get_left_child()
        T2 = x.get_right_child()

        # Rotation
        x.set_right_child(y)
        y.set_left_child(T2)

        # Update parents
        x.set_parent(y.get_parent())
        y.set_parent(x)

        if T2:
            T2.set_parent(y)

        # Adjust reference of the original node's parent
        if x.get_parent() is None:
            tree.root = x
        elif x.get_parent().get_left_child() == y:
            x.get_parent().set_left_child(x)
        else:
            x.get_parent().set_right_child(x)

        # Update heights
        tree._update_height(y)
        tree._update_height(x)

        # Register rotation
        tree.rotations_count['single_right'] += 1

        return x

    @staticmethod
    def rotate_left(tree, x: FlightNode):
        """
        Single left rotation (RR).

            x                         y
           / \                      /   \
          T1  y        ---->      x     T3
             / \                 / \
            T2  T3              T1  T2

        This rotation is applied when the right subtree
        is unbalanced to the right.
        """

        y = x.get_right_child()
        T2 = y.get_left_child()

        # Rotation
        y.set_left_child(x)
        x.set_right_child(T2)

        # Update parents
        y.set_parent(x.get_parent())
        x.set_parent(y)

        if T2:
            T2.set_parent(x)

        # Adjust parent references
        if y.get_parent() is None:
            tree.root = y
        elif y.get_parent().get_left_child() == x:
            y.get_parent().set_left_child(y)
        else:
            y.get_parent().set_right_child(y)

        # Update heights
        tree._update_height(x)
        tree._update_height(y)

        # Register rotation
        tree.rotations_count['single_left'] += 1

        return y

    @staticmethod
    def rotate_left_right(tree, node: FlightNode):
        """
        Double left-right rotation (LR).

        Step 1: left rotation on the left child
        Step 2: right rotation on the current node
        """

        Rotations.rotate_left(tree, node.get_left_child())
        result = Rotations.rotate_right(tree, node)

        tree.rotations_count['double_left'] += 1

        return result

    @staticmethod
    def rotate_right_left(tree, node: FlightNode):
        """
        Double right-left rotation (RL).

        Step 1: right rotation on the right child
        Step 2: left rotation on the current node
        """

        Rotations.rotate_right(tree, node.get_right_child())
        result = Rotations.rotate_left(tree, node)

        tree.rotations_count['double_right'] += 1

        return result
