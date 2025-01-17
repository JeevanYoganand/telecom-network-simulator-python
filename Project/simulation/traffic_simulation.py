import networkx as nx
import pandas as pd
import random
import csv
import os

class TrafficSimulation:
    def __init__(self, network_file):

        import pickle
        with open(network_file, "rb") as f:
            self.network = pickle.load(f)
        print(f"Loaded network with {len(self.network.nodes)} nodes and {len(self.network.edges)} edges.")

    def generate_traffic(self, num_packets=100):
        packet_overview = []
        path_details = []
        nodes = list(self.network.nodes)
        skipped_count = 0

        sources = [node for node in nodes if node.startswith("User")]
        destinations = nodes 

        for packet_number in range(1, num_packets + 1):
            source, destination = random.choice(sources), random.choice(destinations)

            try:
                path = nx.shortest_path(self.network, source=source, target=destination, weight="latency")
                total_latency = sum(self.network[u][v]["latency"] for u, v in zip(path[:-1], path[1:]))
                bandwidth_used = random.randint(1, 100)

                packet_overview.append({
                    "Packet Number": packet_number,
                    "Source Node": source,
                    "Destination Node": destination,
                    "Path": " -> ".join(path),
                    "Total Latency (ms)": total_latency,
                    "Bandwidth Used (Mbps)": bandwidth_used
                })

                for u, v in zip(path[:-1], path[1:]):
                    path_details.append({
                        "Packet Number": packet_number,
                        "From Node": u,
                        "To Node": v,
                        "Bandwidth (Mbps)": self.network[u][v]["bandwidth"]
                    })

                print(f"Packet {packet_number} routed: {source} -> {destination}, Path: {path}")

            except nx.NetworkXNoPath:
                print(f"Packet {packet_number} skipped: No path found between {source} and {destination}")
                skipped_count += 1

        print(f"Total packets: {num_packets}, Routed: {len(packet_overview)}, Skipped: {skipped_count}")
        return packet_overview, path_details

    def save_csv(self, data, file_name):
        if not data:
            print(f"No data to save for {file_name}. Skipping...")
            return
        keys = data[0].keys()
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data saved to {file_name}")

if __name__ == "__main__":

    print("Simulating traffic on the original network (pre-bottleneck)...")
    traffic_sim = TrafficSimulation("results/network.pkl")
    packet_overview, path_details = traffic_sim.generate_traffic(num_packets=100)
    traffic_sim.save_csv(packet_overview, "results/pre_bottleneck_packet_overview.csv")
    traffic_sim.save_csv(path_details, "results/pre_bottleneck_path_details.csv")

    print("\nSimulating traffic on the bottlenecked network (post-bottleneck)...")
    if os.path.exists("results/bottlenecked_network.pkl"):
        traffic_sim = TrafficSimulation("results/bottlenecked_network.pkl")
        packet_overview, path_details = traffic_sim.generate_traffic(num_packets=100)
        traffic_sim.save_csv(packet_overview, "results/post_bottleneck_packet_overview.csv")
        traffic_sim.save_csv(path_details, "results/post_bottleneck_path_details.csv")
    else:
        print("Bottlenecked network file not found. Skipping post-bottleneck simulation.")
