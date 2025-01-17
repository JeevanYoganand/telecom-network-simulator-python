import networkx as nx
import pickle
import os

class NetworkTopology:
    def __init__(self):
        self.network = nx.DiGraph()

    def create_topology(self):
        core_nodes = [f"Core{i}" for i in range(1, 4)]
        regional_nodes = [f"Regional{i}" for i in range(1, 6)]
        access_points = [f"AccessPoint{i}" for i in range(1, 21)]
        cdn_nodes = [f"CDN{i}" for i in range(1, 11)]
        user_devices = [f"User{i}" for i in range(1, 101)]

        self.network.add_nodes_from(core_nodes + regional_nodes + access_points + cdn_nodes + user_devices)

        for i in range(len(core_nodes)):
            for j in range(i + 1, len(core_nodes)):
                self.add_bidirectional_edge(core_nodes[i], core_nodes[j], bandwidth=10000, latency=2)

        for core in core_nodes:
            for regional in regional_nodes:
                self.add_bidirectional_edge(core, regional, bandwidth=5000, latency=5)

        for core in core_nodes:
            for cdn in cdn_nodes:
                self.add_bidirectional_edge(core, cdn, bandwidth=5000, latency=3)

        for i, ap in enumerate(access_points):
            regional = regional_nodes[i % len(regional_nodes)]
            self.add_bidirectional_edge(regional, ap, bandwidth=1000, latency=10)

        for regional in regional_nodes:
            for cdn in cdn_nodes:
                self.add_bidirectional_edge(regional, cdn, bandwidth=1000, latency=5)

        for i, user in enumerate(user_devices):
            ap = access_points[i % len(access_points)]
            self.add_bidirectional_edge(ap, user, bandwidth=200, latency=30)

        print(f"Network created with {len(self.network.nodes)} nodes and {len(self.network.edges)} edges.")

    def add_bidirectional_edge(self, node1, node2, **kwargs):
        self.network.add_edge(node1, node2, **kwargs)
        self.network.add_edge(node2, node1, **kwargs)

    def save_network(self, file_name="results/network.pkl"):
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, "wb") as f:
            pickle.dump(self.network, f)
        print(f"Network saved to {file_name}")

    def check_connectivity(self):
        undirected_network = self.network.to_undirected()
        if nx.is_connected(undirected_network):
            print("The network is fully connected.")
        else:
            print("The network is NOT fully connected.")
            components = list(nx.connected_components(undirected_network))
            print(f"Number of connected components: {len(components)}")

if __name__ == "__main__":
    topology = NetworkTopology()
    topology.create_topology()
    topology.check_connectivity()
    topology.save_network()
