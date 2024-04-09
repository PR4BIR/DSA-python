import queue
import time
import threading

class Server:
    def __init__(self, name):
        self.name = name
        self.status = True

class LoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.request_queue = queue.Queue()
        self.routing_algorithm = self.round_robin
        self.scaling_algorithm = self.time_based_scaling
        self.heartbeat_interval = 5
        self.failover_threshold = 3

    def round_robin(self):
        while True:
            for server in self.servers:
                yield server

    def time_based_scaling(self):
        while True:
            time.sleep(60)  # Check every minute
            # Implement scaling logic here based on server load or other metrics
            # For simplicity, let's assume scaling is not implemented in this example

    def heartbeat_check(self, server):
        while True:
            time.sleep(self.heartbeat_interval)
            if not server.status:
                print(f"Heartbeat failed for server {server.name}. Initiating failover.")
                self.failover(server)

    def failover(self, failed_server):
        failed_server.status = False
        new_server = self.get_next_available_server()
        if new_server:
            print(f"Failover: Replacing {failed_server.name} with {new_server.name}")
            self.request_queue.put(new_server)
            self.start_heartbeat_check(new_server)
        else:
            print("Failover: No available servers. System may experience downtime.")

    def start_heartbeat_check(self, server):
        heartbeat_thread = threading.Thread(target=self.heartbeat_check, args=(server,), daemon=True)
        heartbeat_thread.start()

    def get_next_available_server(self):
        for server in self.routing_algorithm():
            if server.status:
                return server
            time.sleep(0.1)  # Small delay to avoid busy-waiting

    def start_request_processing(self):
        while True:
            server = self.get_next_available_server()
            if server:
                self.request_queue.put(server)
                time.sleep(0.1)  # Small delay to simulate request processing time

    def start(self):
        # Start the scaling algorithm in a separate thread
        scaling_thread = threading.Thread(target=self.scaling_algorithm, daemon=True)
        scaling_thread.start()

        # Start processing requests in the main thread
        self.start_request_processing()

if __name__ == "__main__":
    # Create server instances
    server1 = Server("Server1")
    server2 = Server("Server2")
    server3 = Server("Server3")

    # Create a load balancer with the servers
    load_balancer = LoadBalancer([server1, server2, server3])

    # Start the load balancer
    load_balancer.start()