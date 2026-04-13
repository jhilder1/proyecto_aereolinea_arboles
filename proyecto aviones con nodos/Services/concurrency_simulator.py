from queue import Queue
from models.node import FlightNode

class ConcurrencySimulator:
    """
    Simulates simultaneous insertion flows by handling them
    in a pending requests Queue.
    """
    
    def __init__(self):
        self.pending_queue = Queue()
        
    def enqueue_flight(self, flight_dict):
        """Adds a flight to the pending queue."""
        self.pending_queue.put(flight_dict)
        return self.get_queue_size()
        
    def get_queue_size(self):
        return self.pending_queue.qsize()
        
    def get_pending_flights(self):
        """Returns a list with the current elements of the queue (without popping them)"""
        return list(self.pending_queue.queue)
        
    def process_next(self, tree, flight_controller):
        """
        Processes (dequeues) the next flight and inserts it into the tree.
        Returns information about the inserted node and if it generated critical rebalancing.
        """
        if self.pending_queue.empty():
            return None
            
        flight_dict = self.pending_queue.get()
        
        # Capture how many rotations existed before
        rotations_before = sum(tree.rotations_count.values())
        
        # Insert
        node = flight_controller.create_flight_node(flight_dict)
        tree.insert(node)
        
        # Rotations after
        rotations_after = sum(tree.rotations_count.values())
        rotations_diff = rotations_after - rotations_before
        
        return {
            "flight_inserted": flight_dict["codigo"],
            "rotations_caused": rotations_diff,
            "conflict_alert": rotations_diff > 0 # If there was a rotation, we consider it had a structural impact
        }
        
    def clear_queue(self):
        with self.pending_queue.mutex:
            self.pending_queue.queue.clear()
