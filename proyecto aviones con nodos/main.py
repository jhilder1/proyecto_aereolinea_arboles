from models.avl_tree import AVL
from controller.flight_controller import FlightController
from models.traversals import Traversals
from utils.json_loader import (
    select_json_file,
    load_insert_json,
    load_topology_json
)

def main():

    print("=== AVL FLIGHT SYSTEM ===")

    file_path = select_json_file()

    if not file_path:
        print("No file selected.")
        return

    controller = FlightController()
    tree = AVL()

    try:

        # Try to load as insertion
        flights = load_insert_json(file_path)

        print("\nINSERTION mode detected")

        print("Number of flights:", len(flights))

        controller.insert_flights_into_tree(tree, flights)

    except Exception:

        try:

            # Try to load as topology
            data = load_topology_json(file_path)

            print("\nTOPOLOGY mode detected")

            controller.load_topology_tree(tree, data)

        except Exception as e:

            print("Error loading JSON:", e)
            return


    print("\n=== TREE TRAVERSALS ===")

    print("\nBreadth First Search (BFS):")
    print(Traversals.breadthFirstSearch(tree.root))

    print("\nPreOrder:")
    print(Traversals.preOrderTraversal(tree.root))

    print("\nInOrder:")
    print(Traversals.inOrderTraversal(tree.root))

    print("\nPostOrder:")
    print(Traversals.posOrderTraversal(tree.root))


    print("\n=== TREE INFORMATION ===")

    if tree.root:
        print("Tree height:", tree.root.height)
        print("Root node:", tree.root.get_value())
    else:
        print("The tree is empty.")


if __name__ == "__main__":
    main()
