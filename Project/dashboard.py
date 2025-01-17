import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from simulation.network_topology import NetworkTopology


class Dashboard:
    def __init__(self, network):
        self.network = network

    def visualize_network(self, title="Network Topology"):
        pos = nx.spring_layout(self.network)
        nx.draw(
            self.network,
            pos,
            with_labels=True,
            node_color="lightblue",
            edge_color="gray",
            node_size=2000,
            font_size=10,
        )

        edge_labels = {
            (u, v): f'{d["bandwidth"]}Mbps, {d["latency"]}ms'
            for u, v, d in self.network.edges(data=True)
        }
        nx.draw_networkx_edge_labels(self.network, pos, edge_labels=edge_labels)
        plt.title(title)
        plt.show()

    def visualize_traffic(self, traffic_data_path, title="Traffic Patterns"):
        # Load traffic data
        traffic_data = pd.read_csv(traffic_data_path)

        # Highlight traffic paths on the network
        pos = nx.spring_layout(self.network)
        nx.draw(
            self.network,
            pos,
            with_labels=True,
            node_color="lightblue",
            edge_color="gray",
            node_size=2000,
            font_size=10,
        )

        # Highlight paths
        for _, row in traffic_data.iterrows():
            column_name = "new_path" if "new_path" in traffic_data.columns else "path"
            path = row[column_name].split(" -> ")

            # Highlight the traffic path
            nx.draw_networkx_edges(
                self.network,
                pos,
                edgelist=[(path[i], path[i + 1]) for i in range(len(path) - 1)],
                edge_color="red",
                width=2,
            )

        plt.title(title)
        plt.show()




# Test the Dashboard
if __name__ == "__main__":
    # Create network topology
    topology = NetworkTopology()
    topology.create_topology()

    # Initialize dashboard
    dashboard = Dashboard(topology.network)

    # Visualize network
    dashboard.visualize_network()

    # Visualize normal traffic
    print("Visualizing Normal Traffic...")
    dashboard.visualize_traffic("results/normal_traffic_logs.csv", title="Normal Traffic")

    # Visualize post-bottleneck traffic
    print("Visualizing Post-Bottleneck Traffic...")
    dashboard.visualize_traffic("results/post_bottleneck_traffic_logs.csv", title="Post-Bottleneck Traffic")

    # Visualize rerouted traffic
    print("Visualizing Rerouted Traffic...")
    dashboard.visualize_traffic("results/rerouted_traffic_logs.csv", title="Rerouted Traffic")
