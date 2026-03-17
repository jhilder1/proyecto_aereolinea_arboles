from models.avl_tree import AVL
from controller.flight_controller import FlightController
from models.traversals import Traversals
from utils.json_loader import (
    select_json_file,
    load_insert_json,
    load_topology_json
)

def main():

    print("=== SISTEMA DE VUELOS AVL ===")

    file_path = select_json_file()

    if not file_path:
        print("No se seleccionó ningún archivo.")
        return

    controller = FlightController()
    tree = AVL()

    try:

        # Intentar cargar como inserción
        flights = load_insert_json(file_path)

        print("\nModo INSERCION detectado")

        print("Cantidad de vuelos:", len(flights))

        controller.insert_flights_into_tree(tree, flights)

    except Exception:

        try:

            # Intentar cargar como topología
            data = load_topology_json(file_path)

            print("\nModo TOPOLOGIA detectado")

            controller.load_topology_tree(tree, data)

        except Exception as e:

            print("Error cargando el JSON:", e)
            return


    print("\n=== RECORRIDOS DEL ÁRBOL ===")

    print("\nBreadth First Search (BFS):")
    print(Traversals.breadthFirstSearch(tree.root))

    print("\nPreOrder:")
    print(Traversals.preOrderTraversal(tree.root))

    print("\nInOrder:")
    print(Traversals.inOrderTraversal(tree.root))

    print("\nPostOrder:")
    print(Traversals.posOrderTraversal(tree.root))


    print("\n=== INFORMACIÓN DEL ÁRBOL ===")

    if tree.root:
        print("Altura del árbol:", tree.root.height)
        print("Nodo raíz:", tree.root.get_value())
    else:
        print("El árbol está vacío.")


if __name__ == "__main__":
    main()
