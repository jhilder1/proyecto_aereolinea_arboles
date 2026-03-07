import sys
sys.path.append('.')

from models.node import FlightNode
from models.bst_tree import BST
from models.avl_tree import AVL

def run_tests():
    print("--- INICIANDO PRUEBAS DE ARBOLES ---")
    
    # Nodos de prueba
    flights_data = [
        (10, 100, 50, 0),
        (20, 150, 40, 10),
        (30, 200, 30, 20),
        (40, 250, 20, 30),
        (50, 300, 10, 40)
    ]
    
    bst = BST()
    avl = AVL()

    print("\nInsertando Nodos (10 -> 20 -> 30 -> 40 -> 50) [Causarán desbalanceo hacia la derecha]")
    for data in flights_data:
        # Instanciar nodos separados para no compartir referencias entre árboles
        f_bst = FlightNode(*data)
        f_avl = FlightNode(*data)
        
        bst.insert(f_bst)
        avl.insert(f_avl)

    print("\n--- RESULTADOS ---")
    print(f"Altura BST (esperado 5 - Lineal): {bst.get_height()}")
    print(f"Altura AVL (esperado 3 - Balanceado): {avl.get_height()}")
    
    print(f"Recorrido Anchura BST: {bst.bread_first_search()}")
    print(f"Recorrido Anchura AVL: {avl.bread_first_search()}")
    
    print("\n--- PRUEBA PASADA EXITOSAMENTE SI LAS ALTURAS SON CORRECTAS ---")

if __name__ == '__main__':
    run_tests()
