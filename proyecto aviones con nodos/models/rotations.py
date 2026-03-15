from models.node import FlightNode


class Rotations:
    """
    Clase utilitaria que contiene todas las rotaciones del árbol AVL.

    Se separa del árbol principal para mejorar la modularidad del código.
    Cada método recibe el árbol (tree) y el nodo donde se realizará la rotación.
    """

    @staticmethod
    def rotate_right(tree, y: FlightNode):
        """
        Rotación simple a la derecha (LL).

                y                       x
               / \                    /   \
              x   T3      ---->      T1    y
             / \                         / \
            T1  T2                      T2  T3

        Esta rotación se aplica cuando el subárbol izquierdo
        está desbalanceado hacia la izquierda.
        """

        x = y.get_left_child()
        T2 = x.get_right_child()

        # Rotación
        x.set_right_child(y)
        y.set_left_child(T2)

        # Actualizar padres
        x.set_parent(y.get_parent())
        y.set_parent(x)

        if T2:
            T2.set_parent(y)

        # Ajustar referencia del padre del nodo original
        if x.get_parent() is None:
            tree.root = x
        elif x.get_parent().get_left_child() == y:
            x.get_parent().set_left_child(x)
        else:
            x.get_parent().set_right_child(x)

        # Actualizar alturas
        tree._update_height(y)
        tree._update_height(x)

        # Registrar rotación
        tree.rotations_count['single_right'] += 1

        return x

    @staticmethod
    def rotate_left(tree, x: FlightNode):
        """
        Rotación simple a la izquierda (RR).

            x                         y
           / \                      /   \
          T1  y        ---->      x     T3
             / \                 / \
            T2  T3              T1  T2

        Esta rotación se aplica cuando el subárbol derecho
        está desbalanceado hacia la derecha.
        """

        y = x.get_right_child()
        T2 = y.get_left_child()

        # Rotación
        y.set_left_child(x)
        x.set_right_child(T2)

        # Actualizar padres
        y.set_parent(x.get_parent())
        x.set_parent(y)

        if T2:
            T2.set_parent(x)

        # Ajustar referencias del padre
        if y.get_parent() is None:
            tree.root = y
        elif y.get_parent().get_left_child() == x:
            y.get_parent().set_left_child(y)
        else:
            y.get_parent().set_right_child(y)

        # Actualizar alturas
        tree._update_height(x)
        tree._update_height(y)

        # Registrar rotación
        tree.rotations_count['single_left'] += 1

        return y

    @staticmethod
    def rotate_left_right(tree, node: FlightNode):
        """
        Rotación doble izquierda-derecha (LR).

        Paso 1: rotación izquierda sobre el hijo izquierdo
        Paso 2: rotación derecha sobre el nodo actual
        """

        Rotations.rotate_left(tree, node.get_left_child())
        result = Rotations.rotate_right(tree, node)

        tree.rotations_count['double_left'] += 1

        return result

    @staticmethod
    def rotate_right_left(tree, node: FlightNode):
        """
        Rotación doble derecha-izquierda (RL).

        Paso 1: rotación derecha sobre el hijo derecho
        Paso 2: rotación izquierda sobre el nodo actual
        """

        Rotations.rotate_right(tree, node.get_right_child())
        result = Rotations.rotate_left(tree, node)

        tree.rotations_count['double_right'] += 1

        return result
