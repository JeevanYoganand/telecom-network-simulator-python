import networkx as nx
import pandas as pd
import os
import csv
import pickle

class ResourceReallocation:
    def __init__(self, bottlenecked_network_file):

        with open(bottlenecked_network_file, "rb") as f:
            self.network = pickle.load(f)
        print(f"Loaded bottlenecked network with {len(self.network.nodes)} nodes and {len(self.network.edges)} edges.")

    def reroute_traffic(self, traffic_data_path, output_packet_file, output_path_file):

        traffic_data = pd.read_csv(traffic_data_path)

        rerouted_packet_overview = []
        rerouted_path_details = []

        for _, row in traffic_data.iterrows():
            packet_number = row["Packet Number"]
            source = row["Source Node"]
            destination = row["Destination Node"]

            try:

                path = nx.shortest_path(self.network, source=source, target=destination, weight="latency")
                total_latency = sum(self.network[u][v]["latency"] for u, v in zip(path[:-1], path[1:]))
                bandwidth_used = row["Bandwidth Used (Mbps)"]

                rerouted_packet_overview.append({
                    "Packet Number": packet_number,
                    "Source Node": source,
                    "Destination Node": destination,
                    "Path": " -> ".join(path),
                    "Total Latency (ms)": total_latency,
                    "Bandwidth Used (Mbps)": bandwidth_used
                })

                for u, v in zip(path[:-1], path[1:]):
                    rerouted_path_details.append({
                        "Packet Number": packet_number,
                        "From Node": u,
                        "To Node": v,
                        "Bandwidth (Mbps)": self.network[u][v]["bandwidth"]
                    })

                print(f"Packet {packet_number} rerouted: {source} -> {destination}, Path: {path}")

            except nx.NetworkXNoPath:
                print(f"Packet {packet_number} could not be rerouted: No path found between {source} and {destination}")

        self.save_csv(rerouted_packet_overview, output_packet_file)
        self.save_csv(rerouted_path_details, output_path_file)

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

    reallocator = ResourceReallocation("results/bottlenecked_network.pkl")

    reallocator.reroute_traffic(
        traffic_data_path="results/post_bottleneck_packet_overview.csv",
        output_packet_file="results/rerouted_packet_overview.csv",
        output_path_file="results/rerouted_path_details.csv"
    )
