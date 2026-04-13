import sys
sys.path.append('.')

from models.node import FlightNode
from models.bst_tree import BST
from models.avl_tree import AVL

def run_tests():
    print("--- STARTING TREE TESTS ---")
    
    # Test nodes
    flights_data = [
        (10, 100, 50, 0),
        (20, 150, 40, 10),
        (30, 200, 30, 20),
        (40, 250, 20, 30),
        (50, 300, 10, 40)
    ]
    
    bst = BST()
    avl = AVL()

    print("\nInserting Nodes (10 -> 20 -> 30 -> 40 -> 50) [Will cause right imbalance]")
    for data in flights_data:
        # Instantiate separate nodes so references are not shared between trees
        f_bst = FlightNode(*data)
        f_avl = FlightNode(*data)
        
        bst.insert(f_bst)
        avl.insert(f_avl)

    print("\n--- RESULTS ---")
    print(f"BST Height (expected 5 - Linear): {bst.get_height()}")
    print(f"AVL Height (expected 3 - Balanced): {avl.get_height()}")
    
    print(f"BST Breadth-First Search: {bst.bread_first_search()}")
    print(f"AVL Breadth-First Search: {avl.bread_first_search()}")
    
    print("\n--- TEST PASSED SUCCESSFULLY IF HEIGHTS ARE CORRECT ---")

if __name__ == '__main__':
    run_tests()
