import random
import time
from threading import Thread, Lock

class DistributedNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.data = None
        self.lock = Lock()

    def write_data(self, value):
        with self.lock:
            self.data = value

    def read_data(self):
        with self.lock:
            return self.data


class DistributedSystem:
    def __init__(self):
        self.nodes = [DistributedNode(i) for i in range(3)]

    def simulate_write(self, value):
        print(f"\nWriting '{value}' to nodes")
        for node in self.nodes:
            if random.choice([True, False]):  # Simulate partition
                Thread(target=node.write_data, args=(value,)).start()
            else:
                print(f"Node {node.node_id} partitioned (did not receive update)")

    def simulate_read(self):
        results = []
        for node in self.nodes:
            results.append(node.read_data())
        print(f"Read data from nodes: {results}")

    def run_simulation(self):
        # Simulate write events
        self.simulate_write("Event 1")
        time.sleep(1)  # Simulate time lag

        # Simulate consistency check
        self.simulate_read()

        # Simulate writing another event
        self.simulate_write("Event 2")
        time.sleep(1)

        # Final read
        self.simulate_read()


if __name__ == "__main__":
    system = DistributedSystem()
    system.run_simulation()
